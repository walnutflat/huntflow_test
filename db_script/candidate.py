# -*- coding: utf-8 -*-

"""Класс кандидата.
"""

from dataclasses import dataclass
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
