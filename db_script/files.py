# -*- coding: utf-8 -*-

"""Функции для работы с файлами.
"""

import os
from typing import Optional, List

from db_script import config
from db_script.candidate import Candidate
from db_script.xlsx import parse_db_file

cv_files = {}


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


def get_data_from_files(logger, filenames: list) -> dict:
    """Получить данные о кандидатах из файлов.
    """
    data = {}
    for filename in filenames:
        one_file_data = get_data_from_file(logger, os.path.join(config.folder, filename))
        link_cv(one_file_data)
        data[filename] = one_file_data

    logger.info(f'Сформированы данные из {len(data)} файлов БД')
    return data


def get_data_from_file(logger, filename: str) -> list:
    """Получить данные из одного файла. Обертка для функции парсинга.
    """
    logger.info(f'Обработка файла {filename}')
    res = parse_db_file(logger, filename)
    logger.info(f'Из файла {filename} выбрано {len(res)} записей кандидатов')
    return res


def link_cv(candidates: List[Candidate]) -> None:
    """Привязать пути файлов к списку кандидатов.
    """
    for candidate in candidates:
        if candidate.position not in cv_files:
            cv_dir = os.path.join(config.folder, candidate.position)
            if not os.path.exists(cv_dir):
                continue

            cv_dict = {os.path.splitext(x)[0]: x for x in os.listdir(cv_dir)}
            cv_files[candidate.position] = cv_dict

        cv_path = cv_files[candidate.position].get(candidate.db_name)
        if cv_path:
            cv_path = os.path.join(config.folder, cv_path)

        candidate.cv_path = cv_path



if __name__ == '__main__':
    get_data_from_files(None, config.DB_FOLDER_DEFAULT)
