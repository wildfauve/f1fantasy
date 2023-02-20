from typing import List, Tuple, Union, Any
from functools import partial
from rdflib import Graph, RDF, URIRef, Literal

from f1fantasy import rdf, model
from . import helpers


def find_gp_by_symbol(g: Graph, symbol: str, to_model: bool) -> Union[Tuple, Any]:
    result = helpers.single_result_or_none(rdf.query(g, gp_by_symbol_query(symbol)))
    if not to_model:
        return result
    sub, name, label = result
    return _gp_to_model(subject=sub, name=name, symbolic_name=symbol, label=label)


def find_gp_event_by_symbol_and_season(g: Graph, symbol: str, season: int, to_model: bool = False) -> Union[Tuple, Any]:
    result = helpers.single_result_or_none(rdf.query(g, gp_event_by_symbol_season_query(symbol, season)))
    if not to_model:
        return result
    season_sub, gp_sub, sub = result
    return model.GpEvent(subject=sub,
                         gp=_gp_to_model(subject=gp_sub,
                                         symbolic_name=symbol),
                         season=_season_to_model(subject=season_sub, year=season))


def find_season_by_year(g: Graph, year: int, to_model: bool = False) -> Tuple:
    result = helpers.single_result_or_none(rdf.query(g, season_by_year_query(year)))
    if not to_model:
        return result

    sub, = result
    return _season_to_model(subject=sub, year=year)


def all_seasons(g: Graph):
    return [partial(_season_year, g)(subject) for subject, _, _ in _all_season_types(g)]


def all_gps(g: Graph):
    return [partial(_gp_symbol, g)(subject) for subject, _, _ in _all_gp_types(g)]


def _gp_to_model(subject, name: str = None, symbolic_name: str = None, label: str = None):
    return model.Gp(subject=subject, name=name, symbolic_name=symbolic_name, label=label)

def _season_to_model(subject: URIRef, year: int):
    return model.Season(subject=subject, year=year)


def _season_year(g: Graph, sub: URIRef):
    _, _, yr = rdf.first_matching_triple(g, (sub, rdf.P.fau_f1.forYear, None))
    return yr.toPython()


def _gp_symbol(g: Graph, sub: URIRef):
    _, _, symb = rdf.first_matching_triple(g, (sub, rdf.P.fau_f1.hasSymbol, None))
    return symb.toPython()


def _all_season_types(g) -> List[Tuple]:
    return rdf.all_matching_triples(g, (None, RDF.type, rdf.P.fau_f1.Season))


def _all_gp_types(g) -> List[Tuple]:
    return rdf.all_matching_triples(g, (None, RDF.type, rdf.P.fau_f1.GrandPrix))


# Queries

def gp_by_symbol_query(gp_symbol: str):
    return f"""
    select ?gp ?gp_name ?label 

    where {{
    ?gp a fau-f1:GrandPrix ;
          fau-f1:hasSymbol {Literal(gp_symbol).n3()} ;
          fau-f1:gpName ?gp_name ; 
          skos:prefLabel ?label .
    }}
    """


def season_by_year_query(year: int):
    return f"""
    select ?season 

    where {{
    ?season a fau-f1:Season ;
          fau-f1:forYear {Literal(year).n3()} .
    }}
    """


def gp_event_by_symbol_season_query(symbol, season):
    return f"""
    select ?season ?gp ?ev 

    where {{
    ?season a fau-f1:Season ; 
            fau-f1:forYear {Literal(season).n3()} .

    ?gp a fau-f1:GrandPrix ;
        fau-f1:hasSymbol {Literal(symbol).n3()} .

    ?ev a fau-f1:Formula1GrandPrix ;
        fau-ev:isEventOf ?gp ;
        fau-f1:isForSeason ?season .
    }}
    """
