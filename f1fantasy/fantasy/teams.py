import sys
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

MemberIceTea = member.Member(name="Ice Tea")
MemberGertie = member.Member(name="Gertie")
MemberPepsi = member.Member(name="Pepsi")
MemberRollie = member.Member(name="Rollie")

MemberMarmalade = member.Member(name="Marmalade")
MemberGreenwich = member.Member(name="Greenwich")
MemberRichmond = member.Member(name="Richmond")

MemberRinsky = member.Member(name="Rinksy")

MemberBeetie = member.Member(name="Beetie")
MemberMotzie = member.Member(name="Motzie")

MemberPerky = member.Member(name="Perky")
MemberClaudie = member.Member(name="Claudie")
MemberFyodoro = member.Member(name="Fyodoro")

MemberPiri = member.Member(name="Piri")
MemberEdouard = member.Member(name="Edouard")
MemberPinky = member.Member(name="Pinky")
MemberPurplePerky = member.Member(name="Purple")
MemberSandi = member.Member(name="Sandi")
MemberFlorance = member.Member(name="Florance")

MemberCarter = member.Member(name="Carter")
MemberMorris = member.Member(name="Morris")

# Managed by Juki
TeamGelatoGiants = (fantasy.FantasyTeam(name="TeamGelatoGiants")
                    .has_members([MemberBronzie, MemberLemmie, MemberJuki]))

TeamPolarPrecision = (fantasy.FantasyTeam(name="Polar Precision")
                      .has_members(([MemberIceTea, MemberGertie, MemberRollie, MemberPepsi])))

TeamHeroHangouts = (fantasy.FantasyTeam(name="Hero Hangouts")
                    .has_members([MemberMarmalade, MemberRichmond, MemberGreenwich]))

TeamBearNecessities = (fantasy.FantasyTeam(name="Bear Necessities"))

# Managed by Perky
TeamRinsky = (fantasy.FantasyTeam(name="Rinksy Racing")
              .has_members([MemberRinsky]))

TeamMusicalBears = (fantasy.FantasyTeam(name="Musical Bears").has_members([MemberBeetie, MemberMotzie]))

TeamFauve = (fantasy.FantasyTeam(name="Fauve F1")
             .has_members([MemberPerky]))

TeamClojos = (fantasy.FantasyTeam(name="Clojos")
              .has_members([MemberClaudie, MemberFyodoro]))

TeamLightHouse = (fantasy.FantasyTeam(name="LightHouse.F1")
                  .has_members([MemberPiri,
                                MemberEdouard,
                                MemberSandi,
                                MemberPinky,
                                MemberFlorance,
                                MemberPurplePerky]))

TeamCarterMorris = (fantasy.FantasyTeam(name="carter.morris.racing").has_members([MemberCarter, MemberMorris]))


def teams(g: Graph):
    [add_teams_to_graph(g, team) for team in teams_in_module()]
    return g


def add_teams_to_graph(g, team):
    g.add((team.subject, RDF.type, rdf_prefix.fau_f1.FantasyTeam))
    g.add((team.subject, RDF.type, rdf_prefix.foaf.Group))
    g.set((team.subject, rdf_prefix.foaf.name, Literal(team.name)))
    add_members(g, team.subject, team.members)


def add_members(g, team_subject, members):
    for mem in members:
        s, _, _ = gn.first_matching_triple(g, (mem.subject, None, None))
        if not s:
            g.add((team_subject, rdf_prefix.fau_f1.hasFantasyMembers, mem.subject))
            g.add((mem.subject, RDF.type, rdf_prefix.fau_f1.FantasyMember))
            g.set((mem.subject, FOAF.name, Literal(mem.name)))
        return g


def build_graph(g):
    [team.build_graph(g) for team in teams]


def _team_predicate(team_to_find, team):
    return team_to_find == team


def teams_in_module():
    return [getattr(sys.modules[__name__], name) for name in dir(sys.modules[__name__]) if 'Team' in name]
