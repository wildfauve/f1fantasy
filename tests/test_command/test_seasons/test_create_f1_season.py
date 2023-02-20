from rdflib import Literal, URIRef

from f1fantasy import command
from f1fantasy import model
from f1fantasy import rdf
from f1fantasy import repo


def test_create_season(configure_repo):
    result = command.create_season(2023)

    assert result == model.Result.OK
    assert len(list(repo.graph().triples((None, rdf.P.fau_f1.forYear, Literal(2023))))) == 1


def test_create_season_event(configure_repo, season_2023, create_gp_for_bah):
    result = command.create_season_event(gp_symbol="BAH",
                                         season_year=2023,
                                         gp_date='2023-03-05',
                                         for_round=1)
    assert result == model.Result.OK

    result = rdf.all_matching_triples(repo.graph(), (URIRef('https://fauve.io/f1/grandPrix/2023/BAH'), None, None))

    expected_objs = {'https://fauve.io/ontology/F1/Formula1GrandPrix', 'https://fauve.io/ontology/EVENT/SportsEvent',
                     'https://fauve.io/f1/grandPrix/BAH', 'Bahrain Grand Prix 2023', 'https://fauve.io/f1/season/2023',
                     1, '2023-03-05'}


    assert {r[2].toPython() for r in result} == expected_objs
