# -*- coding: utf-8 -*-

"""Функции для работы с запросами.
"""

import time
from pprint import pprint
from typing import Optional

import requests

from db_script import config


def make_get_request(logger, uri: str, json=None, extra_headers=None, files=None) -> Optional[dict]:
    """Отправить GET запрос, обертка.
    """
    return make_request(logger, 'get', uri, json, extra_headers, files)


def make_post_request(logger, uri: str, json=None, extra_headers=None, files=None) -> Optional[dict]:
    """Отправить POST запрос, обертка.
    """
    return make_request(logger, 'post', uri, json, extra_headers, files)


def make_request(logger, method_name: str, uri: str, json=None,
                 extra_headers=None, files=None) -> Optional[dict]:
    """Отправить запрос, общая функция.
    """
    method = getattr(requests, method_name)
    if not method:
        return None

    headers = {
        'User-Agent': 'App/1.0 (wf88@mail.ru)',
        'Authorization': f'Bearer {config.token}',
    }
    if extra_headers:
        headers = {**headers, **extra_headers}

    response = None

    for attempt in range(1, config.TOTAL_ATTEMPTS + 1):
        # noinspection PyBroadException
        try:
            response = method(
                url=config.API_URL + uri,
                headers=headers,
                json=json,
                files=files,
            )
            break
        except requests.exceptions.ConnectionError as exc:
            logger.warning(f'Ошибка соединения: {exc}')
            logger.info(f'Ожидание {config.SLEEP_SEC} сек')
            time.sleep(config.SLEEP_SEC)
        except Exception as exc:
            logger.error(f'Сбой при обработке запроса: {exc}')
    else:
        logger.error(f'Не удалось обработать запрос')
    if not response:
        logger.warning(f'Проблема с ответом: {response.content}')
        return None

    if response.status_code != 200:
        logger.warning(f'Получен не ОК ответ сервера: {response.content}')
        return None

    return response.json()

