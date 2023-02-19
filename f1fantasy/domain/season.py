from rdflib import Graph, RDF, Literal

from f1fantasy import rdf


def add_season(g: Graph, season):
    _add_gp_to_graph(g, season)
    return g

def _add_gp_to_graph(g, season):
    g.add((season.subject, RDF.type, rdf.P.fau_f1.Season))
    g.set((season.subject, rdf.P.fau_f1.forYear, Literal(season.year)))
    return g
