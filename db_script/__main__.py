from typing import Optional
from loguru import logger
import click as click

from db_script import config
from db_script.files import get_db_files_list, get_data_from_files


@click.command()
@click.option('--token', default=None, help='Токен API')
@click.option('--folder', default=None, help='Директория с БД')
def main(token: Optional[str], folder: Optional[str]):
    """Точка входа.
    """
    logger.add(config.LOG_FILENAME)
    logger.warning('Старт сервиса по переносу данных кандидатов')

    if not token:
        config.token = config.TOKEN_DEFAULT
    if not folder:
        config.folder = config.DB_FOLDER_DEFAULT

    logger.info(f'Параметры: токен = {config.token}, директория с БД = {config.folder}')

    filenames = get_db_files_list(logger, config.folder)
    files_data = get_data_from_files(logger, filenames)






if __name__ == '__main__':
    main()