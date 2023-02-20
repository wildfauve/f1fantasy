from typing import Optional, List
from dataclasses import dataclass, field
from rdflib import URIRef

from . import value


@dataclass
class Season(value.ValueObject):
    year: int
    subject: URIRef = None
    root_uri: str = "https://fauve.io/f1/season/"

    def __post_init__(self):
        if self.subject:
            return self
        self.subject = URIRef(f"{self.root_uri}{self.year}")



@dataclass
class Gp(value.ValueObject):
    name: str = None
    label: str = None
    symbolic_name: str = None
    subject: URIRef = None
    root_uri: str = "https://fauve.io/f1/grandPrix/"

    def __post_init__(self):
        if self.subject:
            return self
        self.subject = URIRef(f"{self.root_uri}{self.symbolic_name}")


@dataclass
class GpEvent(value.ValueObject):
    name: str = None
    season: Season = None
    gp: Gp = None
    round: int = None
    gp_date: str = None
    symbolic_name: str = None
    subject: URIRef = None
    root_uri: str = "https://fauve.io/f1/grandPrix/"

    def __post_init__(self):
        self.name = f"{self.gp.name} {self.season.year}"
        self.symbolic_name = f"{self.gp.symbolic_name}-{self.season.year}"
        self.subject = URIRef(f"{self.root_uri}{self.season.year}/{self.gp.symbolic_name}")
