from rdflib import Graph
from pathlib import Path
from pymonad.reader import Pipe
from functools import partial

from f1fantasy.fantasy import teams
from f1fantasy.f1_seasons import grand_prix, fantasy_scoring
from f1fantasy.repo import triples

triples.RepoContext().configure()


def build(season) -> Graph:
    breakpoint()
    g = save(create_graph(triples.graph(), season))
    return g


def create_graph(g: Graph, season) -> Graph:
    return (Pipe(g)
            .then(teams.teams)
            .then(partial(grand_prix.gps, season))
            .then(partial(fantasy_scoring.scoring, season))
            .flush())


def save(g: Graph):
    triples.save(g)
    return g