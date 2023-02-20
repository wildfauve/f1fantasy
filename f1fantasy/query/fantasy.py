from typing import List, Tuple, Union, Any
from rdflib import Graph, Literal

from f1fantasy import rdf, model
from . import helpers


def find_team_by_name(g: Graph, name: str, to_model: bool = False) -> Union[Tuple, model.FantasyTeam]:
    result = helpers.single_result_or_none(rdf.query(g, team_by_name_query(name)))
    if not to_model:
        return result
    sub, = result
    return model.FantasyTeam(subject=sub, name=name)


def all_teams(g: Graph, to_model: bool = False) -> Union[Tuple, Any]:
    result = rdf.query(g, teams_query())
    if not to_model:
        return result

    return [_to_team_model(team) for team in result]


def _to_team_model(team):
    sub, name, manager = team
    return model.FantasyTeam(subject=sub,
                             name=name.toPython(),
                             manager=manager)


# Queries

def team_by_name_query(name: str):
    return f"""
    select ?team 

    where {{
    ?team a fau-f1:FantasyTeam ;
          foaf:name {Literal(name).n3()} .
    }}
    """

def teams_query():
    return f"""
    select ?team ?team_name ?mgr 

    where {{
    ?team a fau-f1:FantasyTeam ;
          foaf:name ?team_name ;
          fau-f1:isManagedBy ?mgr .
    }}
    """

