from __future__ import annotations

import json
from typing import Any, Dict, List

from .models import ProfileAction, ProfileHero, ProfilePage, ProfileSection, ProfileStat
from .models import DataValidationError


class PayloadValidationError(DataValidationError):
    """Raised when a raw payload fails validation."""


def _require_string(source: Dict[str, Any], field_name: str) -> str:
    value = source.get(field_name)
    if not isinstance(value, str) or not value.strip():
        raise PayloadValidationError(f"{field_name} must be a non-empty string.")
    return value.strip()


def _require_list(source: Dict[str, Any], field_name: str) -> List[Any]:
    value = source.get(field_name)
    if not isinstance(value, list):
        raise PayloadValidationError(f"{field_name} must be a list.")
    return value


def _optional_string(source: Dict[str, Any], field_name: str) -> str | None:
    value = source.get(field_name)
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        raise PayloadValidationError(f"{field_name} must be a non-empty string when provided.")
    return value.strip()


def deserialize_profile_payload(payload: Dict[str, Any]) -> ProfilePage:
    title = _require_string(payload, "title")
    description = _require_string(payload, "description")

    hero_payload = payload.get("hero")
    if not isinstance(hero_payload, dict):
        raise PayloadValidationError("hero must be an object.")

    hero = ProfileHero(
        title=_require_string(hero_payload, "title"),
        lead=_require_string(hero_payload, "lead"),
        eyebrow=_optional_string(hero_payload, "eyebrow"),
        actions=[
            ProfileAction(
                label=_require_string(action, "label"),
                target=_require_string(action, "target"),
                style=_optional_string(action, "style") or "primary",
            )
            for action in _require_list(hero_payload, "actions")
            if isinstance(action, dict)
        ],
        stats=[
            ProfileStat(
                value=_require_string(stat, "value"),
                description=_require_string(stat, "description"),
            )
            for stat in _require_list(hero_payload, "stats")
            if isinstance(stat, dict)
        ],
    )

    sections_payload = _require_list(payload, "sections")
    sections: List[ProfileSection] = []
    for section in sections_payload:
        if not isinstance(section, dict):
            raise PayloadValidationError("Each section must be an object.")
        sections.append(
            ProfileSection(
                section_id=_require_string(section, "section_id"),
                eyebrow=_optional_string(section, "eyebrow"),
                title=_require_string(section, "title"),
                content=_require_string(section, "content"),
                section_type=_require_string(section, "section_type") ,
            )
        )
    return ProfilePage(title=title, description=description, hero=hero, sections=sections)


def serialize_profile_page(page: ProfilePage) -> Dict[str, Any]:
    return {
        "title": page.title,
        "description": page.description,
        "hero": {
            "title": page.hero.title,
            "lead": page.hero.lead,
            "eyebrow": page.hero.eyebrow,
            "actions": [
                {"label": action.label, "target": action.target, "style": action.style}
                for action in page.hero.actions
            ],
            "stats": [
                {"value": stat.value, "description": stat.description}
                for stat in page.hero.stats
            ],
        },
        "sections": [
            {
                "section_id": section.section_id,
                "eyebrow": section.eyebrow,
                "title": section.title,
                "content": section.content,
                "section_type": section.section_type,
            }
            for section in page.sections
        ],
    }


def parse_json_body(raw_body: bytes) -> Dict[str, Any]:
    try:
        payload = json.loads(raw_body.decode("utf-8"))
    except (TypeError, ValueError) as exc:
        raise PayloadValidationError("Request body must be valid JSON.") from exc
    if not isinstance(payload, dict):
        raise PayloadValidationError("Request JSON must be an object.")
    return payload
