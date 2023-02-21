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


def all_teams(g: Graph, to_model: bool = True) -> Union[List[Tuple], List[model.FantasyTeam]]:
    result = rdf.query(g, teams_and_members())
    if not to_model:
        return result

    return [_to_team_with_members(team, props) for team, props in groupby(result, lambda x: x[0])]

def team_scores_by_gp_event(g: Graph,
                            season: int,
                            to_model: bool = True) -> Union[List[Tuple], List[model.FantasyTeamEventScore]]:
    result = rdf.query(g, _team_scores_by_gp_event(Literal(season)))
    if not to_model:
        return result
    return [_team_scores(row) for row in result]

#
# Helpers
#

def _to_team_with_members(team_sub, team_props) -> List[model.FantasyTeam]:
    props_list = list(team_props)
    _, team_name, manager_sub, manager_name, *_ = props_list[0]
    return _to_team_model(
        (
            team_sub,
            team_name,
            _to_member_model(manager_sub, manager_name.toPython()),
            [_to_member_model(mem_sub, mem) for _, _, _, _, mem_sub, mem in props_list]
        ))

def _team_scores(result_row):
    season, year, ev, rd, gp, gp_name, gp_symb, ev_score, score, team, team_name = result_row
    return model.FantasyTeamEventScore(
        for_event=model.GpEvent(subject=ev,
                                for_round=rd.toPython(),
                                season=model.Season(subject=season, year=year.toPython()),
                                gp=model.Gp(subject=gp, name=gp_name.toPython(), symbolic_name=gp_symb.toPython())),
        for_team=model.FantasyTeam(subject=team, name=team_name.toPython()),
        subject=ev_score,
        points=score.toPython())


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


def _team_scores_by_gp_event(year: Literal):
    return f"""

    select ?season ?year ?ev ?round ?gp ?gp_name ?gp_symbol ?ev_score ?score ?team ?team_name 

    where {{
      ?ev a fau-f1:Formula1GrandPrix ;
          fau-f1:isForSeason ?season ;
          fau-f1:isGpRound ?round ;
          fau-ev:isEventOf ?gp .
    
      ?season fau-f1:forYear ?year .

      ?gp skos:prefLabel ?gp_name ;
          fau-f1:hasSymbol ?gp_symbol .

      ?ev_score a fau-f1:FantasyEventScore ;
                fau-f1:isForEvent ?ev ;
                fau-f1:hasEventScore ?score ;
                fau-f1:isForTeam ?team .

      ?team foaf:name ?team_name .  

      filter (?year = {year.n3()}) }}

      ORDER BY ?round
    """