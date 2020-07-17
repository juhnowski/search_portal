import logging

import requests

logger = logging.getLogger(__name__)

BERESTA_URL = "http://master-rsprs.lab50:8080/share/proxy/alfresco-noauth/rsprs/public/nds?flUl=&rows=1000&page={page}&sord=asc"

# Ограничение на кол-во загружаемых страниц. На всякий случай.
MAX_PAGES = 1000


def store_notifications(notifications):
    """Обрабатывает очередную порцию уведомлений.

    :param notifications: Уведомления в формате JSON.
    """
    for notification in notifications:
        # print(notification["@rsprsPrns:prns"])
        pass


def update_notifications():
    print("Синхронизация с Берестой: обновляем уведомления о темах")
    page = 1
    while True:
        url = BERESTA_URL.format(page=page)
        response = requests.get(url)
        if response.status_code != requests.codes.ok:
            break
        data = response.json()
        store_notifications(data["rows"])
        if page == int(data["total"]):
            break
        page += 1
        if page > MAX_PAGES:
            break
