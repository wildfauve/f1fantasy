from functools import partial
import sys
import json
from rdflib import Graph, RDF, Literal

from f1fantasy.graph import rdf_prefix
from f1fantasy.model import gp

BahrainGrandPrix = gp.Gp(name='Bahrain Grand Prix', symbolic_name='BAH', label="Bahrain")
SaudiArabianGrandPrix = gp.Gp(name='Saudi Arabian Grand Prix', symbolic_name='SAU', label="SaudiArabia")
AustralianGrandPrix = gp.Gp(name='Australian Grand Prix', symbolic_name='AUS', label="Australia")
EmiliaRomagnaGrandPrix = gp.Gp(name='Emilia Romagna Grand Prix', symbolic_name='EMR', label="Romagna")
MiamiGrandPrix = gp.Gp(name='Miami Grand Prix', symbolic_name='MIA', label="Miami")
SpanishGrandPrix = gp.Gp(name='Spanish Grand Prix', symbolic_name='SPA', label="Spain")
MonacoGrandPrix = gp.Gp(name='Monaco Grand Prix', symbolic_name='MON', label="Monaco")
AzerbaijanGrandPrix = gp.Gp(name='Azerbaijan Grand Prix', symbolic_name='AZB', label="Azerbaijan")
CanadianGrandPrix = gp.Gp(name='Canadian Grand Prix', symbolic_name='CAN', label="Canada")
BritishGrandPrix = gp.Gp(name='British Grand Prix', symbolic_name='GBR', label="Britian")
AustrianGrandPrix = gp.Gp(name='Austrian Grand Prix', symbolic_name='AUT', label="Austria")
FrenchGrandPrix = gp.Gp(name='French Grand Prix', symbolic_name='FRA', label="France")
HungarianGrandPrix = gp.Gp(name='Hungarian Grand Prix', symbolic_name='HUN', label="Hungary")
BelgianGrandPrix = gp.Gp(name='Belgian Grand Prix', symbolic_name='BEL', label="Belgian")
ItalianGrandPrix = gp.Gp(name='Italian Grand Prix', symbolic_name='ITA', label="Italy")
SingaporeGrandPrix = gp.Gp(name='Singapore Grand Prix', symbolic_name='SIG', label="Singapore")
JapaneseGrandPrix = gp.Gp(name='Japanese Grand Prix', symbolic_name='JAP', label="Japan")
UnitedStatesGrandPrix = gp.Gp(name='United States Grand Prix', symbolic_name='USA', label="USA")
MexicoCityGrandPrix = gp.Gp(name='Mexico City Grand Prix', symbolic_name='MEX', label="Mexico")
BrazilianGrandPrix = gp.Gp(name='Brazilian Grand Prix', symbolic_name='BRA', label="Brazil")
AbuDhabiGrandPrix = gp.Gp(name='Abu Dhabi Grand Prix', symbolic_name='ABD', label="AbuDhabi")
NetherlandsGrandPrix = gp.Gp(name='Netherlands Grand Prix', symbolic_name='NED', label="Netherlands")
QatarGrandPrix = gp.Gp(name='Qatar Grand Prix', symbolic_name='QAT', label="Qatar")
LasVegasGrandPrix = gp.Gp(name='Las Vegas Grand Prix', symbolic_name='LOS', label="LasVegas")

from . import years


def gps(g: Graph):
    [add_gp_to_graph(g, prix) for prix in grand_prix_in_module()]
    [add_events_to_graph(g, year_module) for year_module in years.years]
    return g


def add_gp_to_graph(g, prix):
    g.add((prix.subject, RDF.type, rdf_prefix.fau_f1.GrandPrix))
    g.set((prix.subject, rdf_prefix.fau_f1.gpName, Literal(prix.name)))
    g.set((prix.subject, rdf_prefix.skos.prefLabel, Literal(prix.label)))


def add_events_to_graph(g, year_module):
    return getattr(year_module, "add_events_to_graph")(g)




def grand_prix_in_module():
    return [getattr(sys.modules[__name__], name) for name in dir(sys.modules[__name__]) if 'GrandPrix' in name]
