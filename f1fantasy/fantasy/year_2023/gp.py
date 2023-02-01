from functools import partial
import json
from rdflib import Graph, RDF, Literal, URIRef, FOAF

from f1fantasy.graph import rdf_prefix
from f1fantasy.model import gp
from f1fantasy.fantasy import grand_prix
from f1fantasy.repo import gn
from f1fantasy.util import fn, echo


gps_2023 = [gp.GpEvent(gp=grand_prix.BAHRAIN, year=2023)]


def gp_events(g: Graph):
    [add_gp_to_graph(g, gps_2023) for gp_2023 in gps_2023]
    return g


def add_gp_to_graph(g, gp_2023):
    g.add((gp_2023.subject, RDF.type, rdf_prefix.fau_f1.GrandPrixEvent))
    g.set((gp_2023.subject, rdf_prefix.skos.notation, Literal(gp_2023.gp.name)))
    g.set((gp_2023.subject, rdf_prefix.fau_f1.isInYear, Literal(gp_2023.year)))


def build_graph(g):
    [team.build_graph(g) for team in teams]


def symbolised_names():
    return [t.symbolic_name for t in teams]


def explain_points_for_team(team_name, teams):
    team = find_team_by_name(team_name, teams)
    if not team:
        echo.echo("Team Not Found")
        return None
    echo.echo(json.dumps(team.explain_points(), indent=4))
    pass


def find_team_by_name(team_name, teams):
    return fn.find(partial(_team_name_predicate, team_name), teams)


def find_team(team, teams):
    return fn.find(partial(_team_predicate, team), teams)


def _team_name_predicate(team_name, team):
    return team_name == team.symbolic_name


def _team_predicate(team_to_find, team):
    return team_to_find == team
