from typing import Callable
import sys
from rdflib import Graph, RDF, Literal, FOAF

from f1fantasy import model, rdf, query
from f1fantasy.util import echo
from . import helpers


def show_teams(presenter: Callable):
    presenter(get_teams_and_members(helpers.graph()))


def get_teams_and_members(g):
    return query.all_teams(g)


def add_teams_to_graph(g, team: model.FantasyTeam) -> Graph:
    g.add((team.subject, RDF.type, rdf.P.fau_f1.FantasyTeam))
    g.add((team.subject, RDF.type, rdf.P.foaf.Group))
    g.set((team.subject, rdf.P.foaf.name, Literal(team.name)))
    g.set((team.subject, rdf.P.fau_f1.isManagedBy, team.manager))
    add_members(g, team.subject, team.members)
    return g


def add_members(g, team_subject, members):
    for mem in members:
        if member_in_team(g, team_subject, mem.subject):
            return g
        s, _, _ = rdf.first_matching_triple(g, (mem.subject, None, None))
        g.add((team_subject, rdf.P.fau_f1.hasFantasyMembers, mem.subject))
        g.add((mem.subject, RDF.type, rdf.P.fau_f1.FantasyMember))
        g.set((mem.subject, FOAF.name, Literal(mem.name)))


def member_in_team(g, team_sub, mem_sub):
    return rdf.first_matching_triple(g, (team_sub, rdf.P.fau_f1.hasFantasyMembers, mem_sub)) != (None, None, None)


def build_graph(g):
    [team.build_graph(g) for team in teams]


def _team_predicate(team_to_find, team):
    return team_to_find == team


def teams_in_module():
    return [getattr(sys.modules[__name__], name) for name in dir(sys.modules[__name__]) if 'Team' in name]
