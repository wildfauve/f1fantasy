from typing import Tuple, List, Optional
from functools import partial
from rdflib import Literal, URIRef
import pendulum
from f1fantasy.util import fn, monad


def cond_predicate(term, triple: Tuple) -> bool:
    return triple[1] == term


def object_collection(triple_collection: List[Tuple]):
    return [o for _, _, o in triple_collection]


def object_ind(triple: Tuple):
    _, _, o = triple
    return o


def triple_finder(term, t_map: List[Tuple], filter_fn=fn.find, cond=cond_predicate, builder=object_ind):
    """
    Takes a triples map and applies a filter fn and a condition to return either
    a List[(s,p,o)] or (s,p,o)
    """
    result = filter_fn(partial(cond, term), t_map)
    if result:
        return builder(result)
    return builder((None, None, None))


def first_matching_triple(g, pattern: Tuple) -> Tuple:
    triple_list = list(all_matching_triples(g, pattern))
    if not triple_list:
        return (None, None, None)
    return triple_list[0]


def all_matching_triples(g, pattern: Tuple) -> List[Tuple]:
    return list(g.triples(pattern))


def literal_time(time_literal: Literal) -> Optional[str]:
    if not time_literal:
        return None
    iso_time = safe_time_convert(time_literal)
    return iso_time.value if iso_time.is_right else None


@monad.monadic_try()
def safe_time_convert(time_literal):
    return time_literal.value.isoformat()


@monad.monadic_try()
def safe_time_parser(time_str: str) -> monad.EitherMonad[pendulum.DateTime]:
    return pendulum.parse(time_str)


def price_label(amt: URIRef, ccy: URIRef) -> str:
    # TODO: Add the rdf-cty-ccy lib
    return "{c}{a}".format(c=ccy.split("/")[-1], a=str(amt.value))


def coerce_literal_value(literal: Literal) -> Optional:
    if not hasattr(literal, 'value'):
        return None
    return literal.value


def coerce_uri(uri: URIRef) -> Optional[str]:
    if not hasattr(uri, 'toPython'):
        return uri if isinstance(uri, str) else None
    return uri.toPython()


def month_day_from_nav(navdatetime) -> Tuple[str, str]:
    time = safe_time_convert(navdatetime) >> safe_time_parser
    if time.is_left():
        return None, None
    return time.value.format("YYYY-MM"), time.value.to_date_string()
