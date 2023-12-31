from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from app import db  # noqa
from geoalchemy2.shape import to_shape
from sqlalchemy import  Column, Integer, String


class Person(db.Model):
    __tablename__ = "person"

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    company_name = Column(String, nullable=False)


