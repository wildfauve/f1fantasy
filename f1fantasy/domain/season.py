from rdflib import Graph, RDF, Literal

from f1fantasy import rdf


def add_season(g: Graph, season):
    _add_season_to_graph(g, season)
    return g


def add_gp(g: Graph, prix):
    _add_gp_to_graph(g, prix)
    return g


# Helpers

def _add_season_to_graph(g, season):
    g.add((season.subject, RDF.type, rdf.P.fau_f1.Season))
    g.set((season.subject, rdf.P.fau_f1.forYear, Literal(season.year)))
    return g


def _add_gp_to_graph(g, prix):
    g.add((prix.subject, RDF.type, rdf.P.fau_f1.GrandPrix))
    g.set((prix.subject, rdf.P.fau_f1.gpName, Literal(prix.name)))
    g.set((prix.subject, rdf.P.skos.prefLabel, Literal(prix.label)))
