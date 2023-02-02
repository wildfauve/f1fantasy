from functools import partial
import json
from rdflib import Graph, RDF, Literal

from f1fantasy.graph import rdf_prefix
from f1fantasy.model import gp
from f1fantasy.f1_seasons import grand_prix
from f1fantasy.util import fn, echo



events = [gp.GpEvent(gp=grand_prix.BAHRAIN, year=2023)]
