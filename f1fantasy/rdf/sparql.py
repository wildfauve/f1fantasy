from typing import Callable
from rdflib import Literal
from rdflib.plugins.sparql.processor import SPARQLResult


def sparql_prefixes():
    return """prefix fau-f1: <https://fauve.io/ontology/F1/>
    prefix fau-ev: <https://fauve.io/ontology/EVENT/>
    prefix foaf: <http://xmlns.com/foaf/0.1/>
    prefix skos: <http://www.w3.org/2004/02/skos/core#>
    prefix foaf: <http://xmlns.com/foaf/0.1/>
    """

def query(g, query_exp: str, prefixes_fn: Callable = sparql_prefixes) -> SPARQLResult:
    return g.query(f"{prefixes_fn()}\n{query_exp}")


