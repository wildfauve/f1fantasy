from functools import partial
import json
from rdflib import Graph, RDF, Literal

from f1fantasy.graph import rdf_prefix
from f1fantasy.model import gp
from . import year_2023


BAHRAIN = gp.Gp(name="Bahrain", symbolic_name="BAH")

years = [year_2023]

grand_prix = [BAHRAIN]

def gps(g: Graph):
    [add_gp_to_graph(g, prix) for prix in grand_prix]
    [add_event_to_graph(g, year_events) for year_module in years for year_events in year_module.events.events]
    return g


def add_gp_to_graph(g, prix):
    g.add((prix.subject, RDF.type, rdf_prefix.fau_f1.GrandPrix))
    g.set((prix.subject, rdf_prefix.skos.notation, Literal(prix.name)))


def gp_events(g: Graph):
    [add_gp_to_graph(g, gp_2023) for gp_2023 in gps_2023]
    return g


def add_event_to_graph(g, event_for_year):
    g.add((event_for_year.subject, RDF.type, rdf_prefix.fau_f1.GrandPrixEvent))
    g.add((event_for_year.subject, rdf_prefix.fau_f1.isEventOf, event_for_year.gp.subject))
    g.set((event_for_year.subject, rdf_prefix.skos.notation, Literal(event_for_year.name)))
    g.set((event_for_year.subject, rdf_prefix.fau_f1.isInYear, Literal(event_for_year.year)))
