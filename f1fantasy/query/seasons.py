from typing import List, Tuple
from functools import partial
from rdflib import Graph, RDF, URIRef

from f1fantasy import rdf

def all_seasons(g: Graph):
    return [partial(_season_year, g)(subject) for subject, _, _ in _all_season_types(g)]

def _season_year(g: Graph, sub: URIRef):
    _, _, yr = rdf.first_matching_triple(g, (sub, rdf.P.fau_f1.forYear, None))
    return yr.toPython()


def _all_season_types(g) -> List[Tuple]:
    return rdf.all_matching_triples(g, (None, RDF.type, rdf.P.fau_f1.Season))