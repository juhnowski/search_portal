
Используется python3.7.2

Локальная установка:

1. mkdir portal && cd portal
1. virtualenv .env
1. source .env/bin/activate
1. git clone --recurse-submodules https://gitlab.com/lab50/portal/backend.git
1. cd backend && pip install -r requirements.txt
1. cd infoportal
1. python manage.py makemigrations users documents notes folders search analytics integration && python manage.py migrate
1. python manage.py loaddata fixtures/users.json --app users
1. python manage.py loaddata fixtures/documents.json --app documents
1. python manage.py loaddata fixtures/notes.json --app notes
1. python manage.py loaddata fixtures/folders.json --app folders
1. python manage.py loaddata fixtures/import_journal.json --app integration
1. python index_builder.py
1. python manage.py runserver

Имеется 5 ролей пользователей и superuser (Админ):

    ('GA', 'Админ группы'),
    ('BL', 'Библиотека'),
    ('RD', 'Читатель'),
    ('UR', 'Пользователь'),
    ('EX', 'Эксперт'),

В данный момент все действия, кроме регистрации разрешены только для superuser (Админ)

После загрузки фикстур (python manage.py loaddata ...) создается несколько
пользователей, в том числе Админ. 
Логин/пароль Админа: admin@gmail.com/admin123
Логин/пароль юзера "email1@gmail.com": email1@gmail.com/portal123

при использовании postgresql надо установить расширение pg_trgm
1) sudo -i -u postgres
2) psql -d infoportal
3) CREATE EXTENSION pg_trgm;


Для создания/обновления индекса поиска по БД:
cd backend/infoportal
python index_builder.py
Если в консоли после выполнения будут ошибки связанные с БД, то надо проверить
или изменить настройки БД в файле settings/common.py
Для того чтобы использовать sphinxsearch индексы: необходимо установить sphinxsearch: sudo apt-get install sphinxsearch 
Для ubuntu 19.10 пакет sphinxsearch версия 2.2.11-2build1
Если не будет хватать прав: то клиент sphinxsearch не запустится и в консоли сервера будет строка client = null - это можно исправить расширив права пользователя

Если используется Solr то необходимо вручную выполнить следующие действия:
(если Solr будет выбран в качестве основного движка настройки будут конфигурировать в автоматическом режиме,
скорее всего, это будет копирование настроенных solrconfig.xml, solr.xml и data-config.xml,
 из папки search/engines/haystack/solr_errors/conf)
0) Установка - скачиваем архив: 
https://www.apache.org/dyn/closer.lua/lucene/solr/8.3.1/solr-8.3.1.tgz
распаковываем и в .profile прописываем путь
```
PATH="/home/ilya/solr-8.3.1/bin:$PATH"
```
1) Стартуем Solr
```
solr start
```
2) Создаем core
```
solr create -c infoportal -s 2 -rf 2
```
3) Разрешаем удаленный стриминг:
```
curl -H 'Content-type:application/json' -d '{"set-property": {"requestDispatcher.requestParsers.enableRemoteStreaming": true}, "set-property":{"requestDispatcher.requestParsers.enableStreamBody": true}}' http://localhost:8983/api/collections/infoportal/config
```

4) запускаем
```
python index_builder.py
```

5) запускаем сервер python manage.py runserver
Если все прошло успешно, то в консоли будет лог об успешном тестовом поиске:
```
count = 1 docs=[{'doc_name_ru': 'акустика', 'id': 'c08a095f-e499-4533-b523-3c90d78dbcd2', '_version_': 1653031498083729408}]
```

6) остановка Solr:
```
solr stop -all
```