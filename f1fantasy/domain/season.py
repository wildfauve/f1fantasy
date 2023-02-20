from rdflib import Graph, RDF, Literal

from f1fantasy import rdf, repo


def add_season(g: Graph, season):
    _add_season_to_graph(g, season)
    return g


def add_gp(g: Graph, prix):
    _add_gp_to_graph(g, prix)
    return g


def add_gp_event(g: Graph, event):
    _add_gp_event_to_graph(g, event)
    return g


# Helpers

def _add_season_to_graph(g, season):
    g.add((season.subject, RDF.type, rdf.P.fau_f1.Season))
    g.set((season.subject, rdf.P.fau_f1.forYear, Literal(season.year)))
    return g


def _add_gp_to_graph(g, prix):
    g.add((prix.subject, RDF.type, rdf.P.fau_f1.GrandPrix))
    g.set((prix.subject, rdf.P.fau_f1.gpName, Literal(prix.name)))
    g.set((prix.subject, rdf.P.fau_f1.hasSymbol, Literal(prix.symbolic_name)))
    g.set((prix.subject, rdf.P.skos.prefLabel, Literal(prix.label)))


def _add_gp_event_to_graph(g, event):
    g.add((event.subject, RDF.type, rdf.P.fau_f1.Formula1GrandPrix))
    g.add((event.subject, RDF.type, rdf.P.fau_ev.SportsEvent))
    g.add((event.subject, rdf.P.fau_ev.isEventOf, event.gp.subject))
    g.set((event.subject, rdf.P.fau_ev.label, Literal(event.name)))
    g.set((event.subject, rdf.P.fau_f1.isForSeason, event.season.subject))
    g.set((event.subject, rdf.P.fau_f1.isGpRound, Literal(event.round)))
    g.set((event.subject, rdf.P.fau_f1.hasGpDate, Literal(event.gp_date)))
