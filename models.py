from dataclasses import dataclass, fields


class SkillType:
    def __init__(self, value: str, selected: bool = True, skills: list = None) -> None:
        self.value = value
        self._selected = selected
        if skills is None:
            skills = []
        self.skills = skills

    @property
    def has_enabled_skills(self):
        if not self.skills:
            return False
        return any(skill.selected for skill in self.skills)

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, value):
        if self._selected is False and value is True:
            self._selected = value
            self.activate_skills()
        elif self._selected is True and value is False:
            self._selected = value
            self.deactivate_skills()
        else:
            self._selected = value

    def activate_skills(self):
        for skill in self.skills:
            skill.selected = True

    def deactivate_skills(self):
        for skill in self.skills:
            skill.selected = False

    def __repr__(self) -> str:
        return f"SkillType({self.value}, {self.selected})"

    def __str__(self) -> str:
        return self.value


@dataclass
class Skill:
    value: str
    selected: bool = True

    def __str__(self) -> str:
        return self.value


@dataclass
class Experience:
    date: str
    role: str
    company: str
    location: str
    description: str
    skills: str
    selected: bool = True

    def __str__(self) -> str:
        return f"{self.date}, {self.role}, {self.company}, {self.location}"

    def __iter__(self):
        for field in fields(self):
            yield getattr(self, field.name)


@dataclass
class Education:
    date: str
    title: str
    organization: str
    location: str
    description: str = ""
    selected: bool = True

    def __str__(self) -> str:
        return f"{self.date}, {self.title}, {self.organization}, {self.location}"

    def __iter__(self):
        for field in fields(self):
            yield getattr(self, field.name)


@dataclass
class Certification:
    date: str
    title: str
    organization: str = ""
    selected: bool = True

    def __str__(self) -> str:
        return f"{self.date}, {self.title}, {self.organization}"

    def __iter__(self):
        for field in fields(self):
            yield getattr(self, field.name)
