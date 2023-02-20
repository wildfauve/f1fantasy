from rdflib import Literal

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
    breakpoint()
    assert result == model.Result.OK
    assert len(list(repo.graph().triples((None, rdf.P.fau_f1.forYear, Literal(2023))))) == 1
