import sys

from search.engines.simple.builder import SimpleIndexBuilder
from search.engines.solr.builder import SolrIndexBuilder
from search.engines.sphinx.builder import SphinxIndexBuilder
from search.engines.whoosh.builder import WhooshIndexBuilder
from settings.common import DATABASES, SEARCH_ENGINE

if __name__ == '__main__':
    print("НАЧАЛО ИНДЕКСАЦИИ")
    if SEARCH_ENGINE.get('name') == 'simple':
        ib = SimpleIndexBuilder()

    elif SEARCH_ENGINE.get('name') == 'sphinx':
        if DATABASES.get('default').get('ENGINE') != 'django.db.backends.postgresql_psycopg2':
            print(f"ОШИБКА ИНДЕКСАЦИИ: БД {DATABASES.get('default').get('ENGINE')} не поддерживается sphinx")
            sys.exit()
        else:
            ib = SphinxIndexBuilder()
    elif SEARCH_ENGINE.get('name') == 'solr':
        ib = SolrIndexBuilder()
    elif SEARCH_ENGINE.get('name') == 'whoosh':
        ib = WhooshIndexBuilder()
    else:
        print(f"ОШИБКА ИНДЕКСАЦИИ: не задан движок")
        sys.exit()

    ib.build()
    print("ИНДЕКСАЦИЯ УСПЕШНО ЗАВЕРШЕНА")
