"""Data models for the SQLite database.

The module contains simple dataclasses that mirror the database tables.
They are used only by the tests to provide type hints and to keep the
schema definition in a single place.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Project:
    id: Optional[int]
    name: str
    description: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime


@dataclass
class Setting:
    key: str
    value: str
    updated_at: datetime


@dataclass
class History:
    id: Optional[int]
    action: str
    details: Optional[str]
    created_at: datetime


@dataclass
class Voice:
    id: Optional[int]
    name: str
    provider: str
    language: str
    voice_id: Optional[str]
    created_at: datetime


@dataclass
class Image:
    id: Optional[int]
    project_id: Optional[int]
    prompt: Optional[str]
    file_path: str
    created_at: datetime


@dataclass
class Video:
    id: Optional[int]
    project_id: Optional[int]
    title: Optional[str]
    file_path: str
    duration: float
    created_at: datetime
