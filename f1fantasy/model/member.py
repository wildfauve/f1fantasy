from typing import Optional, List
from dataclasses import dataclass, field
from rdflib import URIRef


from . import value


@dataclass
class Member(value.ValueObject):
    name: str = None
    symbolic_name: str = None
    subject: URIRef = None
    root_uri: str = "https://fauve.io/fantasyMember/"

    def __post_init__(self):
        self.symbolic_name = self.name.replace(" ", "")
        self.subject = URIRef(f"{self.root_uri}{self.symbolic_name}")
