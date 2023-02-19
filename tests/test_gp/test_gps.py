from rdflib import RDF

from f1fantasy.f1_seasons import grand_prix
from f1fantasy.graph import rdf_prefix
from f1fantasy.repo import triples
from f1fantasy.rdf import gn


def test_add_gps_to_graph(configure_repo, empty_graph):
    g = triples.save(grand_prix.gps(empty_graph))

    gp_triples = gn.all_matching_triples(g, (None, RDF.type, rdf_prefix.fau_f1.GrandPrix))

    expected_gp_subs = {'https://fauve.io/f1/grandPrix/BAH'}

    gp_subjects = {s.toPython() for s, _, _ in gp_triples}

    assert gp_subjects == expected_gp_subs


def test_add_gp_events_to_graph(configure_repo, empty_graph):
    g = triples.save(grand_prix.gps(empty_graph))

    ev_triples = gn.all_matching_triples(g, (None, RDF.type, rdf_prefix.fau_f1.GrandPrixEvent))

    expected_ev_subs = {'https://fauve.io/f1/grandPrix/2023/BAH'}

    ev_subjects = {s.toPython() for s, _, _ in ev_triples}

    assert ev_subjects == expected_ev_subs


