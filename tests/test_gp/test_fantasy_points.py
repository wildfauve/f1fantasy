from rdflib import RDF

from f1fantasy.f1_seasons import fantasy_scoring
from f1fantasy.graph import rdf_prefix
from f1fantasy.repo import triples
from f1fantasy.rdf import gn


def test_add_event_points_to_graph(configure_repo, empty_graph):
    g = triples.save(fantasy_scoring.scoring(None, empty_graph))

    pt_triples = gn.all_matching_triples(g, (None, RDF.type, rdf_prefix.fau_f1.FantasyEventScore))

    expected_points_subs = {'https://fauve.io/fantasyTeam/Clojos/EventScore/BAH-2023'}


    pt_subjects = {s.toPython() for s, _, _ in pt_triples}

    assert pt_subjects == expected_points_subs
