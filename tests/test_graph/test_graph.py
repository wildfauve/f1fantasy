from rdflib import Literal

from f1fantasy.f1_seasons import competition
from f1fantasy.graph import sparql

def test_team_gp_points_query(configure_repo, empty_graph):
    g = competition.create_graph(empty_graph)

    result = sparql.query(g, sparql.team_scores_by_gp_event(Literal(2023)))

    rows = list(result)

    breakpoint()