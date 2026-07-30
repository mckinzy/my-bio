from __future__ import annotations

from typing import List

from .models import ProfilePage, ProfileSection, ProfileSection as SectionModel


def summarize_section_titles(page: ProfilePage) -> List[str]:
    return [section.title for section in page.sections]


def find_section_by_type(page: ProfilePage, section_type: str) -> ProfileSection | None:
    return next((section for section in page.sections if section.section_type == section_type), None)


def normalize_page_content(page: ProfilePage) -> ProfilePage:
    """Return a new page object with normalized title and description whitespace."""
    normalized_sections = [
        SectionModel(
            section_id=section.section_id.strip(),
            eyebrow=section.eyebrow.strip() if section.eyebrow else None,
            title=section.title.strip(),
            content=section.content.strip(),
            section_type=section.section_type,
        )
        for section in page.sections
    ]
    normalized_hero = page.hero
    return ProfilePage(
        title=page.title.strip(),
        description=page.description.strip(),
        hero=normalized_hero,
        sections=normalized_sections,
    )
