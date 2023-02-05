from rdflib import Graph
from pathlib import Path
from pymonad.reader import Pipe

from f1fantasy.fantasy import teams
from f1fantasy.f1_seasons import grand_prix, fantasy_scoring
from f1fantasy.repo import triples

triples.Repo().configure()


def load_and_save() -> Graph:
    g = save(load_graph(triples.graph()))
    return g


def load_graph(g: Graph) -> Graph:
    return (Pipe(g)
            .then(teams.teams)
            .then(grand_prix.gps)
            .then(fantasy_scoring.scoring)
            .flush())


def save(g: Graph):
    triples.save(g)
    return g