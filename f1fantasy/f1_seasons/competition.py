from rdflib import Graph
from pathlib import Path
from pymonad.reader import Pipe

from f1fantasy.fantasy import teams
from f1fantasy.f1_seasons import grand_prix, fantasy_scoring
from f1fantasy.repo import triples

triples.Repo().configure()


def load_and_save() -> Graph:
    g = (Pipe(triples.graph())
         .then(teams.teams)
         .then(grand_prix.gps)
         .then(fantasy_scoring.scoring)
         .flush())
    triples.save(g)
    return g
