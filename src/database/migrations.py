"""Database migration definitions.

The migration system is intentionally simple: each integer key maps to a
single SQL statement that creates or alters the database schema.  The
``DatabaseManager`` applies migrations sequentially until the database
reaches :data:`LATEST_VERSION`.
"""

from __future__ import annotations

from typing import Dict

# Current schema version
LATEST_VERSION = 2

# Migration SQL statements
MIGRATIONS: Dict[int, str] = {
    1: """
    -- projects table
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        status TEXT NOT NULL DEFAULT 'draft',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    );

    -- settings table
    CREATE TABLE IF NOT EXISTS settings (
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL,
        updated_at TEXT NOT NULL
    );

    -- history table
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        action TEXT NOT NULL,
        details TEXT,
        created_at TEXT NOT NULL
    );

    -- voices table
    CREATE TABLE IF NOT EXISTS voices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        provider TEXT NOT NULL,
        language TEXT NOT NULL,
        voice_id TEXT,
        created_at TEXT NOT NULL
    );

    -- images table
    CREATE TABLE IF NOT EXISTS images (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER,
        prompt TEXT,
        file_path TEXT NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY(project_id) REFERENCES projects(id) ON DELETE CASCADE
    );

    -- videos table
    CREATE TABLE IF NOT EXISTS videos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER,
        title TEXT,
        file_path TEXT NOT NULL,
        duration REAL DEFAULT 0,
        created_at TEXT NOT NULL,
        FOREIGN KEY(project_id) REFERENCES projects(id) ON DELETE CASCADE
    );
    """,
    2: """
    -- generations table for tracking AI generation jobs
    CREATE TABLE IF NOT EXISTS generations (
        id TEXT PRIMARY KEY,
        category TEXT NOT NULL,
        template_name TEXT NOT NULL,
        variables TEXT NOT NULL,
        media_types TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'pending',
        result TEXT,
        error TEXT,
        created_at TEXT NOT NULL,
        completed_at TEXT,
        duration_ms REAL,
        metadata TEXT
    );
    """,
}
