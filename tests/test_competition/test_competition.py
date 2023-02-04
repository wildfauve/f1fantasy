from rdflib import RDF

from f1fantasy.f1_seasons import competition
from f1fantasy.graph import rdf_prefix


def test_load_and_save_from_declarations():
    g = competition.load_and_save()

    teams = g.triples((None, RDF.type, rdf_prefix.fau_f1.FantasyTeam))

    team_subs = {s.toPython() for s, _, _ in teams}

    assert team_subs == {'https://fauve.io/fantasyTeam/TeamFauve', 'https://fauve.io/fantasyTeam/TeamGelatoGiants',
                         'https://fauve.io/fantasyTeam/TeamLightHouse', 'https://fauve.io/fantasyTeam/TeamMusicalBears',
                         'https://fauve.io/fantasyTeam/TeamClojo'}
