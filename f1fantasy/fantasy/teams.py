from functools import partial
import json
from rdflib import Graph, RDF, Literal, URIRef, FOAF

from f1fantasy.graph import rdf_prefix
from f1fantasy.model import fantasy, member
from f1fantasy.repo import gn
from f1fantasy.util import fn, echo

MemberBronzie = member.Member(name="Bronzie")
MemberJuki = member.Member(name="Juki")
MemberLemmie = member.Member(name="Lemmie")
MemberRinsky = member.Member(name="Rinksy")
MemberBeetie = member.Member(name="Beetie")
MemberMotzie = member.Member(name="Motzie")
MemberPerky = member.Member(name="Perky")
MemberClaudie = member.Member(name="Claudie")
MemberFyodoro = member.Member(name="Fyodoro")
MemberMotzie = member.Member(name="Motzie")
MemberPerky = member.Member(name="Perky")
MemberPiri = member.Member(name="Piri")
MemberEdouard = member.Member(name="Edouard")


TeamGelatoGiants = (fantasy.FantasyTeam(name="TeamGelatoGiants")
                    .has_members([MemberBronzie, MemberLemmie, MemberJuki]))
TeamMusicalBears = (fantasy.FantasyTeam(name="Team Musical Bears")
                    .has_members([MemberBeetie, MemberMotzie, MemberRinsky]))
TeamFauve = (fantasy.FantasyTeam(name="Team Fauve")
             .has_members([MemberPerky]))
TeamClojos = (fantasy.FantasyTeam(name="Team Clojo")
              .has_members([MemberClaudie, MemberFyodoro]))
TeamLightHouse = (fantasy.FantasyTeam(name="Team LightHouse")
                  .has_members([MemberPiri, MemberEdouard]))

fantasy_teams = [TeamGelatoGiants,
                 TeamMusicalBears,
                 TeamClojos,
                 TeamLightHouse,
                 TeamFauve]


def teams(g: Graph):
    [add_teams_to_graph(g, team) for team in fantasy_teams]
    return g


def add_teams_to_graph(g, team):
    t, _, _ = gn.first_matching_triple(g, (team.subject, None, None))
    if t:
        return g
    g.add((team.subject, RDF.type, rdf_prefix.fau_f1.FantasyTeam))
    g.set((team.subject, rdf_prefix.skos.notation, Literal(team.name)))
    add_members(g, team.subject, team.members)


def add_members(g, team_subject, members):
    for mem in members:
        s, _, _ = gn.first_matching_triple(g, (mem.subject, None, None))
        if not s:
            g.add((team_subject, rdf_prefix.fau_f1.hasFantasyMembers, mem.subject))
            g.add((mem.subject, RDF.type, rdf_prefix.fau_f1.FantasyMember))
            g.set((mem.subject, FOAF.name, Literal(member)))
        return g



def member_subject(member):
    return URIRef(f"https://fauve.io/fantasyMember/{member}")


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
