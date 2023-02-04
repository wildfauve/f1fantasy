from functools import partial
import json
from rdflib import Graph, RDF, Literal

from f1fantasy.graph import rdf_prefix

from . import years

def scoring(g: Graph):
    [add_event_score_to_graph(g, year_ev_score) for year_module in years.years for year_ev_score in year_module.scores]
    return g


def add_event_score_to_graph(g, year_ev_score):
    g.add((year_ev_score.subject, RDF.type, rdf_prefix.fau_f1.FantasyEventScore))
    g.add((year_ev_score.subject, rdf_prefix.fau_f1.isEventPointsForTeam, year_ev_score.for_team.subject))
    g.add((year_ev_score.subject, rdf_prefix.fau_f1.isEventPointsForEvent, year_ev_score.for_event.subject))
    g.set((year_ev_score.subject, rdf_prefix.fau_f1.hasFantasyEventScore, Literal(year_ev_score.points)))
    return g
