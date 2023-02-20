from typing import List, Tuple, Union, Any
from rdflib import Graph, Literal
from itertools import groupby

from f1fantasy import rdf, model
from . import helpers


def find_team_by_name(g: Graph, name: str, to_model: bool = False) -> Union[Tuple, model.FantasyTeam]:
    result = helpers.single_result_or_none(rdf.query(g, team_by_name_query(name)))
    if not to_model:
        return result
    sub, = result
    return model.FantasyTeam(subject=sub, name=name)


def all_teams(g: Graph, to_model: bool = True) -> Union[Tuple, Any]:
    result = rdf.query(g, teams_and_members())
    if not to_model:
        return result

    return [_to_team_with_members(team, props) for team, props in groupby(result, lambda x: x[0])]


def _to_team_with_members(team_sub, team_props):
    props_list = list(team_props)
    _, team_name, manager_sub, manager_name, *_ = props_list[0]
    return _to_team_model(
        (
            team_sub,
            team_name,
            _to_member_model(manager_sub, manager_name.toPython()),
            [_to_member_model(mem_sub, mem) for _, _, _, _, mem_sub, mem in props_list]
        ))


def _to_team_model(team):
    sub, name, manager, members = team
    return model.FantasyTeam(subject=sub,
                             name=name.toPython(),
                             manager=manager,
                             members=members)


def _to_member_model(sub, name):
    return model.Member(subject=sub, name=name)


# Queries

def team_by_name_query(name: str):
    return f"""
    select ?team 

    where {{
    ?team a fau-f1:FantasyTeam ;
          foaf:name {Literal(name).n3()} .
    }}
    """



def teams_and_members():
    return f"""
    select ?team ?team_name ?mgr ?mgr_name ?member ?member_name 

    where {{
    ?team a fau-f1:FantasyTeam ;
          foaf:name ?team_name ;
          fau-f1:isManagedBy ?mgr ;
          fau-f1:hasFantasyMembers ?member .
    
    ?mgr foaf:name ?mgr_name .
    
    ?member foaf:name ?member_name .
    }}
    ORDER BY ?team_name
    """
