from rdflib import Graph
from pathlib import Path

from f1fantasy.graph import binding
from f1fantasy.util import singleton

DB_LOCATION = (Path(__file__).parent / "f1fantasy-model.ttl")

class Repo(singleton.Singleton):

    def configure(self, triples_location: Path = DB_LOCATION) -> None:
        self.triples_location = triples_location
        pass



def empty_graph():
    return initgraph()


def graph():
    g = initgraph()
    if Repo().triples_location.exists():
        g.parse(Repo().triples_location)
    return g


def save(g: Graph):
    write_to_ttl(g, file=Repo().triples_location)
    return g


def drop():
    Repo().triples_location.unlink(missing_ok=True)


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
