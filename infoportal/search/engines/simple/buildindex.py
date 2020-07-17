import json
import logging
import math
import re
import sqlite3
import timeit
from sqlite3 import Error

import psycopg2
from django.conf import settings

EXT_NAME = r".json"
LOGGER = logging.getLogger('django')

with open('stopwords.txt', "r") as f:
    stopwords = f.read()

def create_connection():
    print("--------------------------------------------------")
    if settings.DATABASES.get('default').get('ENGINE') == 'django.db.backends.postgresql_psycopg2':
        try:
            settings_port = settings.DATABASES.get('default').get('PORT')
            conn = psycopg2.connect(user=settings.DATABASES.get('default').get('USER'),
                                    password=settings.DATABASES.get('default').get('PASSWORD'),
                                    host=settings.DATABASES.get('default').get('HOST'),
                                    port=settings_port if settings_port else "5432",
                                    database=settings.DATABASES.get('default').get('NAME'))
        except Error as er:
            print(f"POSTGRES: {er}")
    elif settings.DATABASES.get('default').get('ENGINE') == 'django.db.backends.sqlite3':
        try:
            conn = sqlite3.connect(settings.DATABASES.get('default').get('NAME'))
            if 'file:memorydb_default' in settings.DATABASES.get('default').get('NAME'):
                # in test case
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE "documents_documents" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "doc_kind" varchar(255) NOT NULL, "doc_mark" varchar(255) NOT NULL, "doc_name_ru" varchar(512) NOT NULL, "doc_name_en" varchar(512) NOT NULL, "doc_annotation" text NOT NULL, "doc_comment" text NOT NULL, "doc_sys_number" varchar(64) NOT NULL, "doc_full_mark" text NOT NULL, "doc_status" varchar(11) NOT NULL, "application_status" varchar(9) NOT NULL, "doc_reg_date" date NOT NULL, "doc_limit_date" date NOT NULL, "doc_on_rf_use" bool NULL, "classifier_pns" varchar(255) NOT NULL, "doc_assign_org" varchar(255) NOT NULL, "doc_assign_date" date NOT NULL, "doc_reg_text" varchar(255) NOT NULL, "doc_effective_date" date NOT NULL, "doc_restoration_date" date NOT NULL, "doc_enter_org" varchar(255) NOT NULL, "tk_rus" varchar(64) NOT NULL, "org_author_name" varchar(1024) NOT NULL, "mtk_dev" varchar(255) NOT NULL, "keywords" text NOT NULL, "doc_annotation_ru" text NOT NULL, "contains_in_npa_links" bool NOT NULL, "cancel_in_part" text NOT NULL, "doc_o_zsh" varchar(255) NOT NULL, "doc_o_zgo_vch" varchar(255) NOT NULL, "doc_o_zgo" varchar(255) NOT NULL, "doc_o_zsh_vch" varchar(255) NOT NULL, "doc_supplemented" varchar(255) NOT NULL, "doc_supplementing" varchar(255) NOT NULL, "doc_outside_system" text NOT NULL, "doc_html_content" text NOT NULL, "doc_image_content" BLOB NULL, "image_contemt_name" varchar(255) NOT NULL, "doc_pdf_content" BLOB NULL, "pdf_content_name" varchar(255) NOT NULL, "doc_changes" text NOT NULL, "has_document_case" text NOT NULL, "doc_rating" real NOT NULL)
                ''')
                cursor.fetchall()
                cursor.close
        except Error as e:
            print(f"SQLITE: {er}")
    else:
        conn = None

    return conn


class BuildIndex:

    def __init__(self):
        self.tf = {}
        self.df = {}
        self.idf = {}
        self.file_to_terms = self.process_files()
        self.regdex = self.regIndex()
        self.totalIndex = self.execute()
        self.vectors = self.vectorize()
        self.rows = {}
        self.mags = self.magnitudes(self.rows)
        self.populateScores()

    def process_files(self):

        conn = create_connection()

        if conn is None:
            return {}

        try:
            with conn:
                cur = conn.cursor()

                cur.execute("SELECT * FROM documents_documents")
                self.rows = cur.fetchall()
                file_to_terms = {}
                for row in self.rows:
                    pattern = re.compile('[\W_]+')
                    doc_id = row[0]
                    file_to_terms[doc_id] = row[3].lower()
                    file_to_terms[doc_id] = pattern.sub(' ', file_to_terms[doc_id])
                    re.sub(r'[\W_]+', '', file_to_terms[doc_id])
                    file_to_terms[doc_id] = file_to_terms[doc_id].split()
                    file_to_terms[doc_id] = [w for w in file_to_terms[doc_id] if w not in stopwords]
                    # TODO: add morphology like stemmer
                    # file_to_terms[doc_id] = [stemmer.stem_word(w) for w in file_to_terms[file]]
                return file_to_terms
        except Exception as ex:
            LOGGER.error(f"{ex}")
            return {}

    def index_one_file(self, termlist):
        fileIndex = {}
        for index, word in enumerate(termlist):
            if word in fileIndex.keys():
                fileIndex[word].append(index)
            else:
                fileIndex[word] = [index]
        return fileIndex

    def make_indices(self, termlists):
        total = {}
        for filename in termlists.keys():
            total[filename] = self.index_one_file(termlists[filename])
        return total

    def fullIndex(self):
        total_index = {}
        indie_indices = self.regdex
        for filename in indie_indices.keys():
            self.tf[filename] = {}
            for word in indie_indices[filename].keys():
                self.tf[filename][word] = len(indie_indices[filename][word])
                if word in self.df.keys():
                    self.df[word] += 1
                else:
                    self.df[word] = 1
                if word in total_index.keys():
                    if filename in total_index[word].keys():
                        total_index[word][filename].append(indie_indices[filename][word][:])
                    else:
                        total_index[word][filename] = indie_indices[filename][word]
                else:
                    total_index[word] = {filename: indie_indices[filename][word]}
        return total_index

    def vectorize(self):
        vectors = {}
        try:
            for row in self.rows:
                doc_id = row[0]
                vectors[doc_id] = [len(self.regdex[doc_id][word]) for word in self.regdex[doc_id].keys()]
        except Exception as ex:
            LOGGER.error(f"{ex}")

        return vectors

    def document_frequency(self, term):
        if term in self.totalIndex.keys():
            return len(self.totalIndex[term].keys())
        else:
            return 0

    def collection_size(self):
        return len(self.rows)

    def magnitudes(self, rows):
        mags = {}
        for row in rows:
            doc_id = row[0]
            mags[doc_id] = pow(sum(map(lambda x: x ** 2, self.vectors[doc_id])), .5)
        return mags

    def term_frequency(self, term, document):
        return self.tf[document][term] / self.mags[document] if term in self.tf[document].keys() else 0

    def populateScores(self):  # pretty sure that this is wrong and makes little sense.
        for row in self.rows:
            doc_id = row[0]
            for term in self.getUniques():
                self.tf[doc_id][term] = self.term_frequency(term, doc_id)
                if term in self.df.keys():
                    self.idf[term] = self.idf_func(self.collection_size(), self.df[term])
                else:
                    self.idf[term] = 0
        return self.df, self.tf, self.idf

    def idf_func(self, N, N_t):
        if N_t != 0:
            return math.log(N / N_t)
        else:
            return 0

    def generateScore(self, term, document):
        try:
            result = self.tf[document][term] * self.idf[term]
        except:
            result = 0.0
        return result

    def regIndex(self):
        return self.make_indices(self.file_to_terms)

    def getUniques(self):
        return self.totalIndex.keys()

    def execute(self):
        return self.fullIndex()

    def save(self, ext):
        index_filename = r"index" + ext
        regdex_filename = r"regdex" + ext
        tf_filename = r"tf" + ext
        df_filename = r"df" + ext
        idf_filename = r"idf" + ext

        open(index_filename, 'w').close()
        open(regdex_filename, 'w').close()
        open(tf_filename, 'w').close()
        open(df_filename, 'w').close()
        open(idf_filename, 'w').close()

        with open(index_filename, "wb") as f:
            f.write(bytes(json.dumps(self.totalIndex), encoding='utf-8'))
        with open(regdex_filename, "wb") as f:
            f.write(bytes(json.dumps(self.regdex), encoding='utf-8'))
        with open(tf_filename, "wb") as f:
            f.write(bytes(json.dumps(self.tf), encoding='utf-8'))
        with open(df_filename, "wb") as f:
            f.write(bytes(json.dumps(self.df), encoding='utf-8'))
        with open(idf_filename, "wb") as f:
            f.write(bytes(json.dumps(self.idf), encoding='utf-8'))

    def load(self, ext):
        index_filename = r"index" + ext
        regdex_filename = r"regdex" + ext
        tf_filename = r"tf" + ext
        df_filename = r"df" + ext
        idf_filename = r"idf" + ext

        try:
            with open(index_filename, "rb") as f:
                self.totalIndex = json.loads(f.read())
            with open(regdex_filename, "rb") as f:
                self.regdex = json.loads(f.read())
            with open(tf_filename, "rb") as f:
                self.tf = json.loads(f.read())
            with open(df_filename, "rb") as f:
                self.df = json.loads(f.read())
            with open(idf_filename, "rb") as f:
                self.idf = json.loads(f.read())
        except Exception as e:
            pass

        return self


if __name__ == '__main__':
    bi = BuildIndex()
    start = timeit.timeit()
    bi.execute()
    end = timeit.timeit()
    print(f'Время индексирования {end - start} количество слов={len(bi.totalIndex)}')

    start = timeit.timeit()
    bi.save(EXT_NAME)
    end = timeit.timeit()
    print(f'Время сохранения {end - start}')

    bi_new = BuildIndex()
    start = timeit.timeit()
    bi_new.load(EXT_NAME)
    end = timeit.timeit()
    print(f'Время загрузки {end - start}')
