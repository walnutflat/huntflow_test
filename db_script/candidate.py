# -*- coding: utf-8 -*-

"""Класс кандидата.
"""

from dataclasses import dataclass
from functools import cached_property
from typing import Optional


@dataclass
class Candidate:
    """Класс кандидата.
    """
    last_name: Optional[str]
    first_name: Optional[str]
    middle_name: Optional[str]
    position: Optional[str]
    salary: Optional[str]
    comment: Optional[str]
    status: Optional[str]
    db_name: Optional[str]
    cv_path: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    email: Optional[str] = None
    birthday_day: Optional[int] = None
    birthday_month: Optional[int] = None
    birthday_year: Optional[int] = None
    cv_uploaded_id: Optional[int] = None
    photo_id: Optional[int] = None
    added_id: Optional[int] = None

    def update_candidate(self, data):
        phones = data['fields'].get('phones')
        if phones:
            self.phone = phones[0]

        self.email = data['fields'].get('email')

        birthdate = data['fields'].get('birthdate')
        if birthdate:
            self.birthday_day = birthdate.get('day')
            self.birthday_month = birthdate.get('month')
            self.birthday_year = birthdate.get('year')

        self.cv_uploaded_id = data['id']
        photo = data.get('photo')
        if photo:
            self.photo_id = photo.get('id')

    @cached_property
    def payload(self):
        payload = {
            'last_name': self.last_name,
            'first_name': self.first_name,
            'middle_name': self.middle_name,
            'phone': self.phone,
            'email': self.email,
            'position': self.position,
            'company': self.company,
            "money": "100000 руб",
            'birthday_day': self.birthday_day,
            'birthday_month': self.birthday_month,
            'birthday_year': self.birthday_year,
            "photo": self.photo_id,
        }

        if self.cv_uploaded_id:
            payload['externals'] = [
                {
                    'auth_type': 'NATIVE',
                    'files': [
                        {'id': self.cv_uploaded_id}
                    ]
                }
            ]

        return payload
