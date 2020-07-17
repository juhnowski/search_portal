import os
import sys
from pathlib import Path
from string import Template
from subprocess import call

from settings.common import SEARCH_ENGINE, DATABASES


# mkdir ./sdata
# touch searchd.pid
# touch /home/ilya/sdata/ext/binlog.lock
# edit path in sphinx.conf
# скачать словари sdata/dicts
# cp /etc/sphinxsearch
# indexer --all
# searchd --config /etc/sphinx/sphinx.work_example.conf

class SphinxIndexBuilder:

    def __init__(self):
        self.HOST = SEARCH_ENGINE.get('HOST')  # 127.0.0.1
        self.PORT = SEARCH_ENGINE.get('PORT')  # 33959
        self.totalIndex = 0
        self.params = {}

    def configure(self):

        self.params = SEARCH_ENGINE.get('params')

        # DATABASES = {
        #     'default': {
        #         'ENGINE': 'django.db.backends.postgresql_psycopg2',
        #         'NAME': 'infoportal',
        #         'USER': 'infoportal',
        #         'PASSWORD': 'infoportal',
        #         'HOST': 'localhost',
        #         'PORT': '',
        #     }
        # }

        self.params['sql_user'] = DATABASES.get('default').get('USER')
        self.params['sql_host'] = DATABASES.get('default').get('HOST')
        self.params['sql_pass'] = DATABASES.get('default').get('PASSWORD')
        self.params['sql_port'] = DATABASES.get('default').get('PORT')
        if self.params['sql_port'] == '':
            self.params['sql_port'] = "5432"
            print(f"В конфигурационном файле не указан порт бд, выбран по умолчанию 5432")

        self.params['sql_db'] = DATABASES.get('default').get('NAME')
        self.params['listen'] = self.PORT

        if not self.params['path'].startswith('/'):
            self.params['path'] = os.path.dirname(os.path.abspath(__file__)) + "/" + self.params['path']
            if not os.path.exists(self.params['path']):
                os.makedirs(self.params['path'])

        if not self.params['log'].startswith('/'):
            self.params['log'] = os.path.dirname(os.path.abspath(__file__)) + "/" + self.params['log']
            if not os.path.exists(os.path.dirname(self.params['log'])):
                os.makedirs(os.path.dirname(self.params['log']))

        if not self.params['query_log'].startswith('/'):
            self.params['query_log'] = os.path.dirname(os.path.abspath(__file__)) + "/" + self.params['query_log']
            if not os.path.exists(os.path.dirname(self.params['query_log'])):
                os.makedirs(os.path.dirname(self.params['query_log']))

        if not self.params['pid_file'].startswith('/'):
            self.params['pid_file'] = os.path.dirname(os.path.abspath(__file__)) + "/" + self.params['pid_file']
            if not os.path.exists(os.path.dirname(self.params['pid_file'])):
                os.makedirs(os.path.dirname(self.params['pid_file']))

        if not self.params['binlog_path'].startswith('/'):
            self.params['binlog_path'] = os.path.dirname(os.path.abspath(__file__)) + "/" + self.params['binlog_path']
            if not os.path.exists(self.params['binlog_path']):
                os.makedirs(self.params['binlog_path'])

        if not self.params['lemmatizer_base'].startswith('/'):
            self.params['lemmatizer_base'] = os.path.dirname(os.path.abspath(__file__)) + "/" + self.params[
                'lemmatizer_base']
            if not os.path.exists(self.params['lemmatizer_base']):
                os.makedirs(self.params['lemmatizer_base'])
        try:
            with open('search/engines/sphinx/sphinx.template.conf') as filein:
                src = Template(filein.read())
                config = src.substitute(self.params)

                open(self.params['path'] + '/sphinx.conf', 'w').close()
                with open(self.params['path'] + '/sphinx.conf', "wb") as f:
                    f.write(config.encode())

        except Exception as e:
            print(e)
            sys.exit()

    def execute(self):

        script = f"""
        touch {self.params['pid_file']}
        touch {self.params['binlog_path']}/binlog.lock
        cd {self.params['lemmatizer_base']}
        """
        ru_file = Path(self.params['lemmatizer_base'] + '/ru.pak')
        if not ru_file.is_file():
            script = script + """
            curl http://sphinxsearch.com/files/dicts/ru.pak --output ru.pak
            """
        en_file = Path(self.params['lemmatizer_base'] + '/en.pak')
        if not en_file.is_file():
            script = script + """
            curl http://sphinxsearch.com/files/dicts/ru.pak --output en.pak
            """

        script = script + f"""
        indexer --all --config {self.params['path'] + '/sphinx.conf'}
        searchd --config {self.params['path'] + '/sphinx.conf'}
        """

        rc = call(script, shell=True)
        print(f"Выполнение скрипта: {rc}")

    def build(self):
        print('Индексация sphinx')
        print('Конфигурация sphinx.conf')
        self.configure()
        print('Проверка словарей')
        self.execute()
