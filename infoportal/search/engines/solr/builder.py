import json
import sqlite3
from sqlite3 import Error

import psycopg2
from SolrClient import SolrClient
from SolrClient.exceptions import SolrError
from settings.common import SEARCH_ENGINE, DATABASES

TMP_FILENAME = 'solr_import_document_temp.json'


def create_connection():
    print("--------------------------------------------------")
    if DATABASES.get('default').get('ENGINE') == 'django.db.backends.postgresql_psycopg2':
        try:
            settings_port = DATABASES.get('default').get('PORT')
            conn = psycopg2.connect(user=DATABASES.get('default').get('USER'),
                                    password=DATABASES.get('default').get('PASSWORD'),
                                    host=DATABASES.get('default').get('HOST'),
                                    port=settings_port if settings_port else "5432",
                                    database=DATABASES.get('default').get('NAME'))
        except Error as er:
            print(f"POSTGRES: {er}")
    elif DATABASES.get('default').get('ENGINE') == 'django.db.backends.sqlite3':
        try:
            conn = sqlite3.connect(DATABASES.get('default').get('NAME'))
            if 'file:memorydb_default' in DATABASES.get('default').get('NAME'):
                # in test case
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE "documents_documents" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "doc_kind" varchar(255) NOT NULL, "doc_mark" varchar(255) NOT NULL, "doc_name_ru" varchar(512) NOT NULL, "doc_name_en" varchar(512) NOT NULL, "doc_annotation" text NOT NULL, "doc_comment" text NOT NULL, "doc_sys_number" varchar(64) NOT NULL, "doc_full_mark" text NOT NULL, "doc_status" varchar(11) NOT NULL, "application_status" varchar(9) NOT NULL, "doc_reg_date" date NOT NULL, "doc_limit_date" date NOT NULL, "doc_on_rf_use" bool NULL, "classifier_pns" varchar(255) NOT NULL, "doc_assign_org" varchar(255) NOT NULL, "doc_assign_date" date NOT NULL, "doc_reg_text" varchar(255) NOT NULL, "doc_effective_date" date NOT NULL, "doc_restoration_date" date NOT NULL, "doc_enter_org" varchar(255) NOT NULL, "tk_rus" varchar(64) NOT NULL, "org_author_name" varchar(1024) NOT NULL, "mtk_dev" varchar(255) NOT NULL, "keywords" text NOT NULL, "doc_annotation_ru" text NOT NULL, "contains_in_npa_links" bool NOT NULL, "cancel_in_part" text NOT NULL, "doc_o_zsh" varchar(255) NOT NULL, "doc_o_zgo_vch" varchar(255) NOT NULL, "doc_o_zgo" varchar(255) NOT NULL, "doc_o_zsh_vch" varchar(255) NOT NULL, "doc_supplemented" varchar(255) NOT NULL, "doc_supplementing" varchar(255) NOT NULL, "doc_outside_system" text NOT NULL, "doc_html_content" text NOT NULL, "doc_image_content" BLOB NULL, "image_contemt_name" varchar(255) NOT NULL, "doc_pdf_content" BLOB NULL, "pdf_content_name" varchar(255) NOT NULL, "doc_changes" text NOT NULL, "has_document_case" text NOT NULL, "doc_rating" real NOT NULL)
                ''')
                cursor.fetchall()
                cursor.close
        except Error as e:
            print(f"SQLITE: {e}")
    else:
        conn = None

    return conn


class SolrDocument:

    def __init__(self, row):
        self.doc_id = row[0]
        self.doc_kind = row[1].lower()
        self.doc_mark = row[2].lower()
        self.doc_name_ru = row[3].lower()
        self.doc_name_en = row[4].lower()
        self.doc_annotation = row[5].lower()
        self.doc_comment = row[6].lower()
        self.doc_full_mark = row[8].lower()
        self.doc_status = row[9].lower()
        # self.doc_assign_date = row[16]
        # self.doc_effective_date = row[18]
        # self.doc_restoration_date = row[19]
        self.tk_rus = row[21].lower()
        self.mtk_dev = row[23].lower()
        self.keywords = row[24].lower()

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

class SolrIndexBuilder:
    def build(self):
        try:
            CLIENT = SolrClient(SEARCH_ENGINE.get('URL'))
        except SolrError:
            print("Solr не запущен, попробуйте выполнить команду: solr start -e cloud")

        # http://lucene.apache.org/solr/guide/8_2/requestdispatcher-in-solrconfig.html
        # script = """
        # curl - H
        # 'Content-type:application/json' - d
        # '{"set-property":
        # {"requestDispatcher.requestParsers.enableRemoteStreaming": true}, "set-property":{"requestDispatcher.requestParsers.enableStreamBody": true}}'
        # http://localhost:8983/api/collections/infoportal/config
        # """
        # rc = call(script, shell=True)
        # print(f"Выполнение скрипта: {rc}")

        print("СТАТУС КЛАСТЕРА")
        print(f'CLIENT.collections={CLIENT.collections.clusterstatus()}')

        print('ЭКСПОРТ ДОКУМЕНТОВ postres')
        conn = create_connection()

        if conn is None:
            return {}

        try:
            with conn:
                cur = conn.cursor()

                cur.execute("SELECT * FROM documents_documents")
                self.rows = cur.fetchall()

                open(TMP_FILENAME, 'w').close()
                with open(TMP_FILENAME, "wb") as f:
                    f.write(bytes("[", encoding='utf-8'))
                    for row in self.rows:
                        document = SolrDocument(row)
                        f.write(bytes(document.toJSON(), encoding='utf-8'))
                        # print(bytes(json.dumps(document), encoding='utf-8'))
                        # f.write(bytes(json.dumps(document), encoding='utf-8'))
                        f.write(bytes(",", encoding='utf-8'))
                    f.write(bytes("]", encoding='utf-8'))
        except Exception as ex:
            print(f"{ex}")

        print('ИМПОРТ ДОКУМЕНТОВ В Solr')
        CLIENT.local_index('infoportal', TMP_FILENAME)
        #
        # print("ТЕСТОВЫЙ ЗАПРОС")
        # res = CLIENT.query('infoportal', {'q': '*:*'})
        # print(res.get_results_count())
        # print(res.docs)
        # print("Индексация не требуется")
