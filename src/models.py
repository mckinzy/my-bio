from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Literal, Optional

SectionType = Literal["hero", "about", "journey", "work", "values", "contact"]
ActionStyle = Literal["primary", "secondary"]


class DataValidationError(ValueError):
    """Raised when a profile data contract does not validate."""


def _validate_non_empty_string(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise DataValidationError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True)
class ProfileAction:
    label: str
    target: str
    style: ActionStyle = "primary"

    def __post_init__(self) -> None:
        _validate_non_empty_string(self.label, "ProfileAction.label")
        _validate_non_empty_string(self.target, "ProfileAction.target")
        if self.style not in ("primary", "secondary"):
            raise DataValidationError("ProfileAction.style must be 'primary' or 'secondary'.")


@dataclass(frozen=True)
class ProfileStat:
    value: str
    description: str

    def __post_init__(self) -> None:
        _validate_non_empty_string(self.value, "ProfileStat.value")
        _validate_non_empty_string(self.description, "ProfileStat.description")


@dataclass(frozen=True)
class ProfileHero:
    title: str
    lead: str
    eyebrow: Optional[str]
    actions: List[ProfileAction] = field(default_factory=list)
    stats: List[ProfileStat] = field(default_factory=list)

    def __post_init__(self) -> None:
        _validate_non_empty_string(self.title, "ProfileHero.title")
        _validate_non_empty_string(self.lead, "ProfileHero.lead")
        if self.eyebrow is not None and not self.eyebrow.strip():
            raise DataValidationError("ProfileHero.eyebrow must be a non-empty string when provided.")
        if not isinstance(self.actions, list):
            raise DataValidationError("ProfileHero.actions must be a list of ProfileAction objects.")
        if not isinstance(self.stats, list):
            raise DataValidationError("ProfileHero.stats must be a list of ProfileStat objects.")


@dataclass(frozen=True)
class ProfileSection:
    section_id: str
    eyebrow: Optional[str]
    title: str
    content: str
    section_type: SectionType

    def __post_init__(self) -> None:
        _validate_non_empty_string(self.section_id, "ProfileSection.section_id")
        _validate_non_empty_string(self.title, "ProfileSection.title")
        _validate_non_empty_string(self.content, "ProfileSection.content")
        if self.eyebrow is not None and not self.eyebrow.strip():
            raise DataValidationError("ProfileSection.eyebrow must be a non-empty string when provided.")
        if self.section_type not in ("hero", "about", "journey", "work", "values", "contact"):
            raise DataValidationError("ProfileSection.section_type must be a valid SectionType.")


@dataclass(frozen=True)
class ProfilePage:
    title: str
    description: str
    hero: ProfileHero
    sections: List[ProfileSection]

    def __post_init__(self) -> None:
        _validate_non_empty_string(self.title, "ProfilePage.title")
        _validate_non_empty_string(self.description, "ProfilePage.description")
        if not isinstance(self.hero, ProfileHero):
            raise DataValidationError("ProfilePage.hero must be a ProfileHero instance.")
        if not isinstance(self.sections, list) or not self.sections:
            raise DataValidationError("ProfilePage.sections must be a non-empty list of ProfileSection instances.")
        for section in self.sections:
            if not isinstance(section, ProfileSection):
                raise DataValidationError("ProfilePage.sections must contain only ProfileSection instances.")

    def section_ids(self) -> List[str]:
        return [section.section_id for section in self.sections]

    def find_section(self, section_id: str) -> Optional[ProfileSection]:
        for section in self.sections:
            if section.section_id == section_id:
                return section
        return None
