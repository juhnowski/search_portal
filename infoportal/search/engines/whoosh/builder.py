import logging
import os
import sqlite3
import time
from sqlite3 import Error

import psycopg2
from settings.common import SEARCH_ENGINE, DATABASES
from whoosh.fields import *
from whoosh.index import create_in
from whoosh.qparser import QueryParser

LOGGER = logging.getLogger('django')


def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print('{:s} время выполнения {:.3f} ms'.format(f.__name__, (time2 - time1) * 1000.0))

        return ret

    return wrap


@timing
def test(ix):
    with ix.searcher() as searcher:
        query = QueryParser("doc_name_ru", ix.schema).parse("акустика")
        results = searcher.search(query)

        print(f'Test request results={results[0].get("doc_id")}')


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


class WhooshIndexBuilder:

    def __init__(self):
        self.INDEX_DIR = SEARCH_ENGINE.get('indexdir')
        self.rows = {}
        print(f'self.INDEX_DIR={self.INDEX_DIR}')
        if not self.INDEX_DIR.startswith('/'):
            self.INDEX_DIR = os.path.dirname(os.path.abspath(__file__)) + "/" + self.INDEX_DIR
            if not os.path.exists(self.INDEX_DIR):
                os.makedirs(self.INDEX_DIR)
        print(f'self.INDEX_DIR={self.INDEX_DIR}')

    def build(self):
        schema = Schema(
            doc_id=NUMERIC(stored=True),
            doc_kind=TEXT(stored=True),
            doc_mark=TEXT(stored=True),
            doc_name_ru=TEXT(stored=True),
            doc_name_en=TEXT(stored=True),
            doc_annotation=TEXT(stored=True),
            doc_comment=TEXT(stored=True),
            doc_full_mark=TEXT(stored=True),
            doc_status=TEXT(stored=True),
            tk_rus=TEXT(stored=True),
            mtk_dev=TEXT(stored=True),
            keywords=KEYWORD(stored=True),
            # doc_assign_date=DATE(stored=True),
            # doc_effective_date=DATE(stored=True),
            # doc_restoration_date=DATE(stored=True),
        )

        conn = create_connection()

        if conn is None:
            return {}

        ix = create_in(self.INDEX_DIR, schema)
        writer = ix.writer()

        try:
            with conn:
                cur = conn.cursor()

                cur.execute("SELECT * FROM documents_documents")
                self.rows = cur.fetchall()

                for row in self.rows:
                    doc_id = row[0]
                    doc_kind = row[1].lower()
                    doc_mark = row[2].lower()
                    doc_name_ru = row[3].lower()
                    doc_name_en = row[4].lower()
                    doc_annotation = row[5].lower()
                    doc_comment = row[6].lower()
                    doc_full_mark = row[8].lower()
                    doc_status = row[9].lower()
                    # doc_assign_date = row[16]
                    # doc_effective_date = row[18]
                    # doc_restoration_date = row[19]
                    tk_rus = row[21].lower()
                    mtk_dev = row[23].lower()
                    keywords = row[24].lower()

                    writer.add_document(
                        doc_id=doc_id,
                        doc_kind=doc_kind,
                        doc_mark=doc_mark,
                        doc_name_ru=doc_name_ru,
                        doc_name_en=doc_name_en,
                        doc_annotation=doc_annotation,
                        doc_comment=doc_comment,
                        doc_full_mark=doc_full_mark,
                        doc_status=doc_status,
                        # doc_assign_date=doc_assign_date,
                        # doc_effective_date = doc_effective_date,
                        # doc_restoration_date = doc_restoration_date,
                        tk_rus=tk_rus,
                        mtk_dev=mtk_dev,
                        keywords=keywords
                    )
                writer.commit()
        except Exception as ex:
            LOGGER.error(f"{ex}")

        test(ix)
        test(ix)
