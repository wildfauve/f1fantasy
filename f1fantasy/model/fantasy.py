from typing import Optional, List
from dataclasses import dataclass, field
from rdflib import URIRef


from . import value


@dataclass
class FantasyTeam(value.ValueObject):
    name: str = None
    members: Optional[List] = field(default_factory=list)
    symbolic_name: str = None
    subject: URIRef = None
    root_uri: str = "https://fauve.io/fantasyTeam/"

    def __post_init__(self):
        self.symbolic_name = self.name.replace(" ", "")
        self.subject = URIRef(f"{self.root_uri}{self.symbolic_name}")

    def has_members(self, membership: List[str]):
        self.members = membership
        return self
