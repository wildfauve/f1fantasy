from rdflib import Literal

from f1fantasy import command
from f1fantasy import model
from f1fantasy import rdf
from f1fantasy import repo

def test_create_gp(configure_repo):
    result = command.create_gp('Bahrain Grand Prix', 'BAH', "Bahrain")

    assert result == model.Result.OK

    assert len(list(repo.graph().triples((None, rdf.P.fau_f1.gpName,  Literal("Bahrain Grand Prix"))))) == 1

