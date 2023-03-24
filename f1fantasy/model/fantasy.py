from typing import Optional, List
from dataclasses import dataclass, field
from rdflib import URIRef


from . import value, gp

@dataclass
class Member(value.ValueObject):
    name: str = None
    symbolic_name: str = None
    subject: URIRef = None
    root_uri: str = "https://fauve.io/fantasyMember/"

    def __post_init__(self):
        self.symbolic_name = self.name.replace(" ", "")
        if self.subject:
            return self
        self.subject = URIRef(f"{self.root_uri}{self.symbolic_name}")

    def __lt__(self, other):
        # For the sorted function to compare
        return self.name < other.name


@dataclass
class FantasyTeam(value.ValueObject):
    name: str = None
    members: Optional[List[Member]] = field(default_factory=list)
    manager: Optional[URIRef] = None
    symbolic_name: str = None
    subject: URIRef = None
    root_uri: str = "https://fauve.io/fantasyTeam/"

    def __post_init__(self):
        self.symbolic_name = self.name.replace(" ", "")
        if self.subject:
            return self
        self.subject = URIRef(f"{self.root_uri}{self.symbolic_name}")

    def has_members(self, membership: List[Member]):
        self.members = membership
        return self


@dataclass
class FantasyTeamEventScore(value.ValueObject):
    for_event: gp.GpEvent = None
    for_team: FantasyTeam = None
    subject: URIRef = None
    points: int = None

    def __post_init__(self):
        if self.subject:
            return self
        self.subject = URIRef(f"{self.for_team.subject.toPython()}/EventScore/{self.for_event.symbolic_name}")


def event_score_from_aggregate(for_team, for_event, points, df):
    if not df.columns[1:]:
        return event_score_per_race(for_team, for_event, points, df)
    breakpoint()

def event_score_per_race(for_team, for_event, points, df):
    return FantasyTeamEventScore(for_team=for_team, for_event=for_event, points=points)