import json
import copy
import logging

import requests

logger = logging.getLogger(__name__)


class AlfrescoError(Exception):
    """ Ошибка, возникшая при обращении к Alfresco API. """
    pass


class AlfrescoApi(object):
    """
    Обёртка вокруг API Alfresco.
    Еще есть какая-то библиотека alfREST, но она не устанавливается.
    """

    URL = 'http://{authority}{path}'
    LOGIN_PATH = '/alfresco/service/api/login'
    LOGOUT_PATH = '/alfresco/service/api/login/ticket/{ticket}'
    SEARCH_PATH = '/alfresco/api/-default-/public/search/versions/1/search'
    CONTENT_PATH = '/alfresco/service/api/node/content/workspace/SpacesStore/{uuid}'

    # Стандартные заголовки HTTP-запроса.
    HEADERS = {'Content-type': 'application/json; charset=utf-8'}
    # Таймаут по умолчанию (в секундах).
    DEFAULT_TIMEOUT = 30

    # Шаблон поискового запроса. Не забываем делать deepcopy.
    SEARCH_QUERY = {
        'query': {'query': None, 'language': 'lucene'},
        'fields': ['id', "name", 'nodeType'],
        'include': ['properties'],
        'paging': {'maxItems': 5000, 'skipCount': 0}
    }
    # Используется при построении поисковых запросов, когда пробелы запрещены.
    WHITESPACE = '_x0020_'

    def __init__(self, host, port):
        """
        :param host: Хост.
        :param port: Порт, на котором работает Alfresco.
        """
        self._authority = host + ':' + str(port)
        self._ticket = None

    def _send_request(self, f, path, error_msg, **kwargs):
        """
        Обёртка вокруг библиотеки requests. Кидается AlfrescoError.

        :param f: Функция библиотеки requests (get, post или delete).
        :param path: Путь, начинающийся с '/'.
        :param error_msg: Сообщение об ошибке без точки на конце.
        :param kwargs: Аргументы для функции f.
        :return: Результат функции f.
        """
        url = self.URL.format(authority=self._authority, path=path)
        if 'timeout' not in kwargs:
            kwargs['timeout'] = self.DEFAULT_TIMEOUT
        try:
            response = f(url, **kwargs)
        except requests.exceptions.ConnectionError:
            raise AlfrescoError(
                '{}: не удалось подключиться к {}.'.format(error_msg, url)
            )
        except requests.exceptions.ReadTimeout:
            raise AlfrescoError(
                '{}: таймаут при подключении к {}.'.format(error_msg, url)
            )

        if response.status_code != requests.codes.ok:
            raise AlfrescoError(
                '{}: код {} от {}.'.format(error_msg, response.status_code, url)
            )
        return response

    def isAuthorized(self):
        """
        :return: True, если мы авторизованы, иначе False.
        """
        return self._ticket is not None

    def login(self, username, password):
        """
        Выполняет авторизацию в Alfresco API.
        :param username: Имя пользователя.
        :param password: Пароль.
        """
        response = self._send_request(
            requests.post, self.LOGIN_PATH,
            'Не удалось авторизоваться в Alfresco',
            json={'username': username, 'password': password},
            headers=self.HEADERS
        )
        self._ticket = response.json()['data']['ticket']

    def logout(self):
        """ Разлогинивается. """
        self._send_request(
            requests.delete,
            self.LOGOUT_PATH.format(ticket=self._ticket),
            'Не удалось разлогиниться',
            params={'alf_ticket': self._ticket}
        )
        self._ticket = None

    def get_node_content(self, uuid):
        """
        Получает контент узла Alfresco.

        :param uuid: Ид узла в формате UUID.
        :return: Контент узла.
        """
        return self._send_request(
            requests.get,
            self.CONTENT_PATH.format(uuid=uuid),
            'Не удалось получить содержимое узла Alfresco',
            params={'alf_ticket': self._ticket}
        ).content

    def search(self, query, properties_required=False, skip=0):
        """
        Выполняет поиск.

        :param query: Запрос на Lucene в виде строки.
        :param properties_required: Выкачивать свойства узлов?
        :param skip: Сколько результатов пропустить?
        :return: Ответ в виде JSON (найденные узлы Alfresco).
        """
        payload = copy.deepcopy(self.SEARCH_QUERY)
        payload['query']['query'] = query
        payload['paging']['skipCount'] = skip
        if not properties_required:
            del payload['include']
        return self._send_request(
            requests.post, self.SEARCH_PATH, 'Ошибка при поиске',
            params={'alf_ticket': self._ticket},
            json=payload,
            headers=self.HEADERS
        ).json()
