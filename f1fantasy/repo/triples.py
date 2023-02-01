from rdflib import Graph
from pathlib import Path

from f1fantasy.graph import binding

BASE_PATH = (Path(__file__).parent / "f1fantasy-model.ttl")


def empty_graph():
    return initgraph()


def graph():
    g = initgraph()
    if BASE_PATH.exists():
        g.parse(BASE_PATH)
    return g


def save(g: Graph):
    write_to_ttl(g, file=BASE_PATH)
    return g


def initgraph() -> Graph:
    return binding.bind(rdf_graph())


def rdf_graph():
    return Graph()


def write_to_ttl(g, format="turtle", file=None):
    if format == "turtle":
        txt = g.serialize(format=format)
    else:
        txt = g.serialize(format="json-ld", indent=4)
    if file:
        with open(file, 'w') as f:
            f.write(txt)
