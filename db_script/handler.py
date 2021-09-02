# -*- coding: utf-8 -*-

"""Основной обработчик.
"""

from loguru import logger

from db_script import config
from db_script.api import get_vacancies, get_statuses, upload_and_parse_file, add_candidate, add_candidate_to_vacancy
from db_script.files import get_db_files_list, get_data_from_files
from db_script.stateholder import StateHolder


@logger.catch()
def handle(logger, restore: bool) -> None:
    """Функция-обработчик.
    """
    sh = StateHolder()
    if restore:
        logger.info('Запуск с восстановлением')
        sh.restore()
        logger.info(f'Восстановлено: {sh.payload}')

    if not sh.files_data:
        logger.info('Запуск парсинга файлов')
        filenames = get_db_files_list(logger, config.folder)
        files_data = get_data_from_files(logger, filenames)
        sh.update_files_data(files_data)
    else:
        logger.info('Данные парсинга восстановлены, запуск не требуется')
        files_data = sh.files_data

    if not sh.vacancies:
        logger.info('Получение вакансий')
        vacancies = get_vacancies(logger)
        sh.update_vacancies(vacancies)
    else:
        logger.info('Список вакансий восстановлен, запуск не требуется')
        vacancies = sh.vacancies

    if not sh.statuses:
        logger.info('Получение статусов')
        statuses = get_statuses(logger)
        sh.update_statuses(statuses)
    else:
        logger.info('Статусы восстановлены, запуск не требуется')
        statuses = sh.statuses

    if any([
        not vacancies,
        not statuses,
    ]):
        logger.error('Не получены вспомогательные данные, завершаем скрипт')
        return

    handle_candidates(sh, logger, files_data, vacancies, statuses)


def handle_candidates(sh: StateHolder, logger, files_data, vacancies, statuses) -> None:
    """Обработать в API кандидатов.
    """
    if not sh.progress:
        progress = {x: 0 for x in files_data}
    else:
        progress = sh.progress

    for filename, candidates in files_data.items():
        if progress[filename] >= len(candidates):
            logger.info(f'Файл {filename} загружен полностью, пропускаем')
            continue

        logger.info(f'Загрузка и обработка данных кандидатов из файла {filename}')
        for num, candidate in enumerate(candidates):
            if num < progress[filename]:
                logger.info(f'Кандидат с индексом {num} обработан, пропускаем')
                continue

            logger.info(f'Обработка кандидата {candidate.db_name}')
            if candidate.cv_path:
                logger.info('Файл резюме найден, загружаем')
                parsed = upload_and_parse_file(logger, candidate.cv_path)
                if parsed:
                    candidate.update_candidate(parsed)
                    sh.update_files_data(files_data)
                    logger.info(f'Файл загружен, данные кандидата обновлены')

            logger.info('Добавляем кандидата')
            added = add_candidate(logger, candidate)
            if not added or added.get('id') is None:
                logger.warning(f'Кандидат не добавлен, прекращаем его обработку')
                continue

            candidate.added_id = added.get('id')
            logger.info('Кандидат добавлен')

            vacancy_id = vacancies.get(candidate.position)
            status_id = statuses.get(candidate.status)

            if any([
                vacancy_id is None,
                status_id is None
            ]):
                logger.warning(f'Нет вспомогательных данных для кандидата (id вакансии {vacancy_id}, '
                               f'id статуса {status_id}), прекращаем обработку кандидата')

            logger.info(f'Добавление кандидата на вакансию')
            added_vacancy = add_candidate_to_vacancy(logger, candidate, vacancy_id, status_id)
            if not added_vacancy or added_vacancy.get('id') is None:
                logger.warning(f'Кандидат не добавлен на вакансию, прекращаем его обработку')
                continue

            logger.success(f'Обработка кандидата {candidate.db_name} успешно завершена!')
            progress[filename] += 1
            sh.update_progress(progress)
        logger.info(f'Обработка кандидатов из файла {filename} завершена')

