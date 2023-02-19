from rdflib import Literal

from f1fantasy import command
from f1fantasy import model
from f1fantasy import rdf
from f1fantasy import repo

def test_create_season(configure_repo):
    result = command.create_season(2023)

    assert result == model.Result.OK
    assert len(list(repo.graph().triples((None, rdf.P.fau_f1.forYear, Literal(2023))))) == 1

