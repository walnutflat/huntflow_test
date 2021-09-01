import os
from typing import Optional, List

from db_script import config
from db_script.candidate import Candidate
from db_script.xlsx import parse_db_file


def get_db_files_list(logger, folder: str) -> List[Optional[str]]:
    """Сформировать список походящих файлов в указанной папке.
     """
    filenames = []

    # noinspection PyBroadException
    try:
        files_list = os.listdir(folder)
    except Exception as exc:
        logger.error(f'Сбой во время получения списка файлов: {exc}')
        files_list = []

    for file in files_list:
        if file.endswith('.xlsx'):
            filenames.append(file)

    logger.info(f'Получено {len(filenames)} имен файлов')
    return filenames


def get_data_from_files(logger, filenames: list):
    data = {}
    for filename in filenames:
        one_file_data = get_data_from_file(logger, f'{config.folder}/{filename}')  #TODO
        data[filename] = one_file_data

    print(data)
    return data


def get_data_from_file(logger, filename: str):
    return parse_db_file(logger, filename)

def link_resume(candidate: Candidate):
    position_folder = f'{config.folder}/{candidate.position}/'




if __name__ == '__main__':
    get_data_from_files(None, config.DB_FOLDER_DEFAULT)

