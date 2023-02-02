from typing import Optional, List
from dataclasses import dataclass, field
from rdflib import URIRef


from . import value


@dataclass
class Gp(value.ValueObject):
    name: str = None
    symbolic_name: str = None
    subject: URIRef = None
    root_uri: str = "https://fauve.io/f1/grandPrix/"

    def __post_init__(self):
        self.subject = URIRef(f"{self.root_uri}{self.symbolic_name}")


@dataclass
class GpEvent(value.ValueObject):
    name: str = None
    year: str = None
    gp: str = None
    subject: URIRef = None
    root_uri: str = "https://fauve.io/f1/grandPrix/"

    def __post_init__(self):
        self.name = f"{self.gp.name} {self.year}"
        self.subject = URIRef(f"{self.root_uri}{self.year}/{self.gp.symbolic_name}")

