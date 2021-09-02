# -*- coding: utf-8 -*-

"""Точка входа.
"""

from typing import Optional

import click as click
from loguru import logger

from db_script import config
from db_script.handler import handle


@logger.catch()
@click.command()
@click.option('--token', default=None, help='Токен API')
@click.option('--folder', default=None, help='Директория с БД')
@click.option('--restore', default=False, help='Восстановиться из дампа', is_flag=True)
def main(token: Optional[str], folder: Optional[str], restore: bool):
    """Точка входа.
    """
    logger.add(config.LOG_FILENAME)
    logger.warning('Старт сервиса по переносу данных кандидатов')

    if token:
        config.token = token
    if folder:
        config.folder = folder

    logger.info(f'Параметры: токен = {config.token}, директория с БД = {config.folder}, '
                f'восстановление = {restore}')
    try:
        handle(logger, restore)
    finally:
        logger.warning('Сервис завершил работу')


if __name__ == '__main__':
    main()
