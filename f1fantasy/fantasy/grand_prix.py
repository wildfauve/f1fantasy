from functools import partial
import json
from rdflib import Graph, RDF, Literal, URIRef, FOAF

from f1fantasy.graph import rdf_prefix
from f1fantasy.model import gp
from f1fantasy.repo import gn
from f1fantasy.util import fn, echo


BAHRAIN = gp.Gp(name="Bahrain", symbolic_name="BAH")
