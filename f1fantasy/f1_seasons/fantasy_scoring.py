from typing import Optional
from functools import partial
import json
from rdflib import Graph, RDF, Literal

from f1fantasy.graph import rdf_prefix

from . import season

def scoring(for_season: Optional[int] = None, g: Optional[Graph] = None):
    if g is None:
        return g
    for season_module in season.seasons:
        if for_season and season_module.season == for_season:
            add_scores_for_season(g, season_module.scores)
            continue
        add_scores_for_season(g, season_module.scores)
    return g

def add_scores_for_season(g, scores):
    for season_event_score in scores:
        add_event_score_to_graph(g, season_event_score)
    return g

def add_event_score_to_graph(g, year_ev_score):
    g.add((year_ev_score.subject, RDF.type, rdf_prefix.fau_f1.FantasyEventScore))
    g.add((year_ev_score.subject, rdf_prefix.fau_f1.isForTeam, year_ev_score.for_team.subject))
    g.add((year_ev_score.subject, rdf_prefix.fau_f1.isForEvent, year_ev_score.for_event.subject))
    g.set((year_ev_score.subject, rdf_prefix.fau_f1.hasEventScore, Literal(year_ev_score.points)))
    return g
