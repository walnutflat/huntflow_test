# -*- coding: utf-8 -*-

"""Конфигурация.
"""

DB_FOLDER_DEFAULT = 'D:\Тестовое задание'
TOKEN_DEFAULT = '71e89e8af02206575b3b4ae80bf35b6386fe3085af3d4085cbc7b43505084482'

API_URL = 'https://dev-100-api.huntflow.dev/'

token = TOKEN_DEFAULT
folder = DB_FOLDER_DEFAULT

LOG_FILENAME = 'db_script.log'

DB_POSITION_COL = 1
DB_NAME_COL = 2
DB_SALARY_COL = 3
DB_COMMENT_COL = 4
DB_STATUS_COL = 5

ACCOUNT_ID = 2
TOTAL_ATTEMPTS = 3
SLEEP_SEC = 5

GET_VACANCIES_URI = f'account/{ACCOUNT_ID}/vacancies'
GET_STATUSES_URI = f'account/{ACCOUNT_ID}/vacancy/statuses'
POST_UPLOAD_FILE = f'account/{ACCOUNT_ID}/upload'
POST_ADD_CANDIDATE = f'account/{ACCOUNT_ID}/applicants'
POST_ADD_CANDIDATE_TO_VACANCY = f'account/{ACCOUNT_ID}/applicants/{{candidate_id}}/vacancy'


MIME_TYPES = {
    '.doc': 'application/msword',
    '.pdf': 'application/pdf',
}

DUMP_FILENAME = 'sh.dump'
