import json
import math
import re
import sqlite3
from sqlite3 import Error

import psycopg2
from settings.common import DATABASES, SEARCH_ENGINE


class SimpleIndexBuilder:

    def __init__(self):
        self.EXT_NAME = SEARCH_ENGINE.get('EXT_NAME')  # r".json"
        self.DB_FILE_NAME = SEARCH_ENGINE.get('DB_FILE_NAME')  # r"db.sqlite3"

        self.tf = {}
        self.df = {}
        self.idf = {}
        self.file_to_terms = self.process_files()
        self.regdex = self.regIndex()
        self.totalIndex = self.execute()
        self.vectors = self.vectorize()
        self.mags = self.magnitudes(self.rows)
        self.populateScores()

    def create_connection(self, db_file):
        conn = None
        if (db_file == r"postgres"):
            try:
                conn = psycopg2.connect(user=DATABASES.get('default').get('USER'),
                                        password=DATABASES.get('default').get('PASSWORD'),
                                        host=DATABASES.get('default').get('HOST'),
                                        port="5432",
                                        database=DATABASES.get('default').get('NAME'))
            except Error as er:
                print(er)
        else:
            try:
                conn = sqlite3.connect(db_file)
            except Error as e:
                print(e)

        return conn

    def process_files(self):

        if DATABASES.get('default').get('ENGINE') == 'django.db.backends.sqlite3':
            try:
                db_name = self.DB_FILE_NAME
            except Exception as ex:
                print(f"{ex}")
        else:
            try:
                db_name = r"postgres"
            except Exception as ex:
                print(f"{ex}")

        conn = self.create_connection(db_name)

        with open('stopwords.txt', "r") as f:
            stopwords = f.read()

        with conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM documents_documents")
            self.rows = cur.fetchall()
            file_to_terms = {}
            for row in self.rows:
                pattern = re.compile('[\W_]+')
                doc_id = row[0]
                text_for_index = row[2] + " " + row[3] + " " + row[5] + " " + row[8]
                file_to_terms[doc_id] = text_for_index.lower()
                file_to_terms[doc_id] = pattern.sub(' ', file_to_terms[doc_id])
                re.sub(r'[\W_]+', '', file_to_terms[doc_id])
                file_to_terms[doc_id] = file_to_terms[doc_id].split()
                file_to_terms[doc_id] = [w for w in file_to_terms[doc_id] if w not in stopwords]
                # TODO: add morphology like stemmer
                # file_to_terms[doc_id] = [stemmer.stem_word(w) for w in file_to_terms[file]]
            return file_to_terms

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
        for row in self.rows:
            doc_id = row[0]
            vectors[doc_id] = [len(self.regdex[doc_id][word]) for word in self.regdex[doc_id].keys()]
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

        return self

    def build(self):
        print('Индексация simple')
        self.execute()
        self.save(self.EXT_NAME)
        print(f'Проиндексировано слов={len(self.totalIndex)}')
