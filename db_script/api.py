# -*- coding: utf-8 -*-

"""Функции для работы с API.
"""

import os
from typing import Optional

from db_script import config
from db_script.candidate import Candidate
from db_script.rq import make_get_request, make_post_request


def get_vacancies(logger) -> Optional[dict]:
    """Получить словарь с вакансиями.
    """
    vacancies = {}
    response = make_get_request(
        logger=logger,
        uri=config.GET_VACANCIES_URI,
    )
    if not response:
        logger.warning('Не получен список вакансий с API')
        return vacancies

    for each in response['items']:
        vacancies[each['position']] = each['id']

    logger.info(f'Из API получено {len(vacancies)} вакансий.')
    return vacancies


def get_statuses(logger) -> Optional[dict]:
    """Получить словарь со статусами.
    """
    statuses = {}
    response = make_get_request(
        logger=logger,
        uri=config.GET_STATUSES_URI,
    )
    if not response:
        logger.warning('Не получен список статусов из API')
        return statuses

    for each in response['items']:
        statuses[each['name']] = each['id']

    logger.info(f'Из API получено {len(statuses)} статусов.')
    return statuses


def upload_and_parse_file(logger, path) -> Optional[int]:
    """Загрузить и распарсить файл резюме, вернуть все данные.
    """
    extra_headers = {
        'X-File-Parse': 'true',
    }

    with open(path, 'rb') as file:
        _, ext = os.path.splitext(path)
        basename = os.path.basename(path)
        mime_type = config.MIME_TYPES.get(ext)
        if not mime_type:
            logger.warning(f'Неизвестный тип файла {ext}')
            return None

        files = {'file': (basename, file, mime_type, {'Expires': '0'})}
        response = make_post_request(
            logger=logger,
            uri=config.POST_UPLOAD_FILE,
            extra_headers=extra_headers,
            files=files,
        )

    return response


def add_candidate(logger, candidate: Candidate) -> Optional[dict]:
    """Добавить кандидата по API.
    """
    response = make_post_request(
        logger=logger,
        uri=config.POST_ADD_CANDIDATE,
        json=candidate.payload
    )

    return response


def add_candidate_to_vacancy(logger, candidate: Candidate, vacancy_id: int, status_id: int) -> Optional[dict]:
    """Добавить кандидата на вакансию.
    """
    json = {
        'vacancy': vacancy_id,
        'status': status_id,
        'comment': candidate.comment,
        'files': [
            {
                "id": candidate.cv_uploaded_id,
            }
        ],
    }
    response = make_post_request(
        logger=logger,
        uri=config.POST_ADD_CANDIDATE_TO_VACANCY.format(candidate_id=candidate.added_id),
        json=json
    )

    return response


