from functools import partial
import sys
import json
from rdflib import Graph, RDF, Literal

from f1fantasy.graph import rdf_prefix
from f1fantasy.model import gp
from f1fantasy.f1_seasons import grand_prix
from f1fantasy.util import fn, echo

BahrainGrandPrix_2023 = gp.GpEvent(gp=grand_prix.BahrainGrandPrix, year=2023, gp_date='2023-03-05', round=1)
SaudiArabianGrandPrix_2023 = gp.GpEvent(gp=grand_prix.SaudiArabianGrandPrix, year=2023, gp_date='2023-', round=2)
AustralianGrandPrix_2023 = gp.GpEvent(gp=grand_prix.AustralianGrandPrix, year=2023, gp_date='2023-', round=3)
EmiliaRomagnaGrandPrix_2023 = gp.GpEvent(gp=grand_prix.EmiliaRomagnaGrandPrix, year=2023, gp_date='2023-', round=6)
MiamiGrandPrix_2023 = gp.GpEvent(gp=grand_prix.MiamiGrandPrix, year=2023, gp_date='2023-', round=5)
SpanishGrandPrix_2023 = gp.GpEvent(gp=grand_prix.SpanishGrandPrix, year=2023, gp_date='2023-', round=8)
MonacoGrandPrix_2023 = gp.GpEvent(gp=grand_prix.MonacoGrandPrix, year=2023, gp_date='2023-', round=7)
AzerbaijanGrandPrix_2023 = gp.GpEvent(gp=grand_prix.AzerbaijanGrandPrix, year=2023, gp_date='2023-', round=4)
CanadianGrandPrix_2023 = gp.GpEvent(gp=grand_prix.CanadianGrandPrix, year=2023, gp_date='2023-', round=9)
BritishGrandPrix_2023 = gp.GpEvent(gp=grand_prix.BritishGrandPrix, year=2023, gp_date='2023-', round=11)
AustrianGrandPrix_2023 = gp.GpEvent(gp=grand_prix.AustrianGrandPrix, year=2023, gp_date='2023-', round=10)
FrenchGrandPrix_2023 = gp.GpEvent(gp=grand_prix.FrenchGrandPrix, year=2023, gp_date='2023-', round=1)
HungarianGrandPrix_2023 = gp.GpEvent(gp=grand_prix.HungarianGrandPrix, year=2023, gp_date='2023-', round=12)
BelgianGrandPrix_2023 = gp.GpEvent(gp=grand_prix.BelgianGrandPrix, year=2023, gp_date='2023-', round=13)
ItalianGrandPrix_2023 = gp.GpEvent(gp=grand_prix.ItalianGrandPrix, year=2023, gp_date='2023-', round=15)
SingaporeGrandPrix_2023 = gp.GpEvent(gp=grand_prix.SingaporeGrandPrix, year=2023, gp_date='2023-', round=16)
JapaneseGrandPrix_2023 = gp.GpEvent(gp=grand_prix.JapaneseGrandPrix, year=2023, gp_date='2023-', round=17)
UnitedStatesGrandPrix_2023 = gp.GpEvent(gp=grand_prix.UnitedStatesGrandPrix, year=2023, gp_date='2023-', round=1)
MexicoCityGrandPrix_2023 = gp.GpEvent(gp=grand_prix.MexicoCityGrandPrix, year=2023, gp_date='2023-', round=20)
BrazilianGrandPrix_2023 = gp.GpEvent(gp=grand_prix.BrazilianGrandPrix, year=2023, gp_date='2023-', round=21)
AbuDhabiGrandPrix_2023 = gp.GpEvent(gp=grand_prix.AbuDhabiGrandPrix, year=2023, gp_date='2023-', round=23)
NetherlandsGrandPrix_2023 = gp.GpEvent(gp=grand_prix.NetherlandsGrandPrix, year=2023, gp_date='2023-08-27', round=14)
QatarGrandPrix_2023 = gp.GpEvent(gp=grand_prix.QatarGrandPrix, year=2023, gp_date='2023-10-08', round=18)
LasVegasGrandPrix_2023 = gp.GpEvent(gp=grand_prix.LasVegasGrandPrix, year=2023, gp_date='2023-11-18', round=22)

year_events = [getattr(sys.modules[__name__], name) for name in dir(sys.modules[__name__]) if 'GrandPrix_2023' in name]

# year_events = [BahrainGrandPrix_2023,
#                SaudiArabianGrandPrix_2023,
#                AustrianGrandPrix_2023,
#                AzerbaijanGrandPrix_2023,
#                MiamiGrandPrix_2023,
#                EmiliaRomagnaGrandPrix_2023,
#                MonacoGrandPrix_2023,
#                SpanishGrandPrix_2023,
#                CanadianGrandPrix_2023,
#                AustrianGrandPrix_2023,
#                BritishGrandPrix_2023,
#                HungarianGrandPrix_2023,
#                BelgianGrandPrix_2023,
#                NetherlandsGrandPrix_2023,
#                ItalianGrandPrix_2023,
#                SingaporeGrandPrix_2023,
#                JapaneseGrandPrix_2023,
#                QatarGrandPrix_2023,
#                UnitedStatesGrandPrix_2023,
#                MexicoCityGrandPrix_2023,
#                BrazilianGrandPrix_2023,
#                LasVegasGrandPrix_2023,
#                AbuDhabiGrandPrix_2023]
