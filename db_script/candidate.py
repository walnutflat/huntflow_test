from dataclasses import dataclass
from typing import Optional


@dataclass
class Candidate:
    last_name: Optional[str]
    first_name: Optional[str]
    middle_name: Optional[str]
    position: Optional[str]
    salary: Optional[str]
    comment: Optional[str]
    status: Optional[str]

