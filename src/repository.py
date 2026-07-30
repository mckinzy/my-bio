from __future__ import annotations

import json
import sqlite3
from typing import Any

from .adapters.db import ConnectionPool, DatabaseConnectionError
from .models import ProfileAction, ProfileHero, ProfilePage, ProfileSection, ProfileStat
from .validation import deserialize_profile_payload, serialize_profile_page, PayloadValidationError


class RepositoryError(Exception):
    pass


class ProfileRepository:
    def __init__(self, pool: ConnectionPool) -> None:
        self.pool = pool
        self._ensure_schema()

    def _ensure_schema(self) -> None:
        self.pool.execute(
            """
            CREATE TABLE IF NOT EXISTS profile_pages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                hero_title TEXT NOT NULL,
                hero_lead TEXT NOT NULL,
                hero_eyebrow TEXT,
                hero_actions TEXT NOT NULL,
                hero_stats TEXT NOT NULL,
                sections TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            fetch=False,
        )

    def save(self, payload: dict[str, Any]) -> int:
        try:
            page = deserialize_profile_payload(payload)
        except PayloadValidationError as exc:
            raise RepositoryError(f"Invalid profile payload: {exc}") from exc

        serialized = serialize_profile_page(page)
        connection = self.pool.acquire()
        try:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO profile_pages (title, description, hero_title, hero_lead, hero_eyebrow, hero_actions, hero_stats, sections) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    serialized["title"],
                    serialized["description"],
                    serialized["hero"]["title"],
                    serialized["hero"]["lead"],
                    serialized["hero"]["eyebrow"],
                    json.dumps(serialized["hero"]["actions"]),
                    json.dumps(serialized["hero"]["stats"]),
                    json.dumps(serialized["sections"]),
                ),
            )
            connection.commit()
            return cursor.lastrowid
        except sqlite3.Error as exc:
            raise RepositoryError("Database write failed.") from exc
        finally:
            self.pool.release(connection)

    def find_by_id(self, record_id: int) -> ProfilePage | None:
        rows = self.pool.execute(
            "SELECT title, description, hero_title, hero_lead, hero_eyebrow, hero_actions, hero_stats, sections FROM profile_pages WHERE id = ? LIMIT 1",
            (record_id,),
            fetch=True,
        )
        if not rows:
            return None

        title, description, hero_title, hero_lead, hero_eyebrow, hero_actions, hero_stats, sections = rows[0]
        hero_actions_data = json.loads(hero_actions)
        hero_stats_data = json.loads(hero_stats)
        sections_data = json.loads(sections)
        return ProfilePage(
            title=title,
            description=description,
            hero=ProfileHero(
                title=hero_title,
                lead=hero_lead,
                eyebrow=hero_eyebrow,
                actions=[
                    ProfileAction(
                        label=action["label"],
                        target=action["target"],
                        style=action.get("style", "primary"),
                    )
                    for action in hero_actions_data
                ],
                stats=[
                    ProfileStat(value=stat["value"], description=stat["description"])
                    for stat in hero_stats_data
                ],
            ),
            sections=[
                ProfileSection(
                    section_id=section["section_id"],
                    eyebrow=section.get("eyebrow"),
                    title=section["title"],
                    content=section["content"],
                    section_type=section["section_type"],
                )
                for section in sections_data
            ],
        )
