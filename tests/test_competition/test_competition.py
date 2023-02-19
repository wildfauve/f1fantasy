from rdflib import RDF

from f1fantasy.f1_seasons import competition
from f1fantasy.graph import rdf_prefix


def test_load_and_save_from_declarations():
    g = competition.build()

    teams = g.triples((None, RDF.type, rdf_prefix.fau_f1.FantasyTeam))

    team_subs = {s.toPython() for s, _, _ in teams}

    assert team_subs == {'https://fauve.io/fantasyTeam/FauveF1', 'https://fauve.io/fantasyTeam/RinksyRacing',
                         'https://fauve.io/fantasyTeam/PolarPrecision', 'https://fauve.io/fantasyTeam/MusicalBears',
                         'https://fauve.io/fantasyTeam/Clojos', 'https://fauve.io/fantasyTeam/TeamGelatoGiants',
                         'https://fauve.io/fantasyTeam/HeroHangouts',
                         'https://fauve.io/fantasyTeam/carter.morris.racing',
                         'https://fauve.io/fantasyTeam/BearNecessities', 'https://fauve.io/fantasyTeam/LightHouse.F1'}
