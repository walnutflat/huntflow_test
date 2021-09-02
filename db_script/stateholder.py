# -*- coding: utf-8 -*-

"""Класс-держатель статуса.
"""

import pickle

from db_script import config


class StateHolder:
    """Класс-держатель статуса.
    """
    def __init__(self):
        self.payload = {}
        self.filename = config.DUMP_FILENAME

    def restore(self):
        """Попытаться восстановиться из дампа.
        """
        try:
            with open(self.filename, mode='rb') as file:
                self.payload = pickle.load(file)
        except:
            pass

    def dump(self):
        """Сохраниться в дамп.
        """
        with open(self.filename, mode='wb') as file:
            pickle.dump(self.payload, file)

    def update_files_data(self, files_data: dict):
        """Обновить данные файлов и сохраниться.
        """
        self.payload['files_data'] = files_data
        self.dump()

    def update_vacancies(self, vacancies: dict):
        """Обновить вакансии и сохраниться.
        """
        self.payload['vacancies'] = vacancies
        self.dump()

    def update_statuses(self, statuses: dict):
        """Обновить статусы и сохраниться.
        """
        self.payload['statuses'] = statuses
        self.dump()

    def update_progress(self, progress: dict):
        """Обновить прогресс и сохраниться.
        """
        self.payload['progress'] = progress
        self.dump()

    def get_parameter(self, parameter: str):
        """Получить произсольный параметр из payload.
        """
        if self.payload:
            return self.payload.get(parameter)

        return None

    @property
    def files_data(self):
        """Сохраненные данные из файлов.
        """
        return self.get_parameter('files_data')

    @property
    def vacancies(self):
        """Сохраненные вакансии.
        """
        return self.get_parameter('vacancies')

    @property
    def statuses(self):
        """Сохраненные статусы.
        """
        return self.get_parameter('statuses')

    @property
    def progress(self):
        """Сохраненный прогресс.
        """
        return self.get_parameter('progress')
