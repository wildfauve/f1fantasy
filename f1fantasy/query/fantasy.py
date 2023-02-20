from typing import List, Tuple, Union, Any
from rdflib import Graph, Literal

from f1fantasy import rdf, model
from . import helpers


def find_team_by_name(g: Graph, name: str, to_model: bool = False) -> Union[Tuple, Any]:
    result = helpers.single_result_or_none(rdf.query(g, team_by_name_query(name)))
    if not to_model:
        return result
    sub, = result
    return model.FantasyTeam(subject=sub, name=name)


# Queries

def team_by_name_query(name: str):
    return f"""
    select ?team 

    where {{
    ?team a fau-f1:FantasyTeam ;
          foaf:name {Literal(name).n3()} .
    }}
    """

