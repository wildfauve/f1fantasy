from rdflib import URIRef, RDF

from f1fantasy import repo
from f1fantasy import rdf


def test_loads_empty_graph(configure_repo):
    assert len(list(repo.graph().subjects())) == 0

def test_saves_graph(configure_repo):
    g = repo.graph()

    g.add((URIRef("https://test.nz/subject/1"), RDF.type, rdf.P.fau_f1.TestClassType))

    repo.save()

    repo.reload()

    g2 = repo.graph()

    assert id(g) != id(g2)
    assert len(list(repo.graph().subjects())) == 1
