from functools import partial
from rdflib import Graph, RDF, Literal

from f1fantasy.graph import rdf_prefix
from f1fantasy.model import gp, fantasy
from f1fantasy.fantasy import teams
from . import events


scores = [
    fantasy.FantasyTeamEventScore(for_event=events.BahrainGrandPrix_2023, for_team=teams.TeamClojos, points=100)
]
