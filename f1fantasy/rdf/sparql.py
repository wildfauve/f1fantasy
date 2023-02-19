from rdflib import Literal
from rdflib.plugins.sparql.processor import SPARQLResult


def query(g, query_exp: str) -> SPARQLResult:
    return g.query(query_exp)

def sparql_prefixes():
    return """prefix fau-f1: <https://fauve.io/ontology/F1/>
    prefix fau-ev: <https://fauve.io/ontology/EVENT/>
    prefix foaf: <http://xmlns.com/foaf/0.1/>
    prefix skos: <http://www.w3.org/2004/02/skos/core#>
    prefix foaf: <http://xmlns.com/foaf/0.1/>

    """

def team_scores_by_gp_event(season: Literal):
    return f"""
    {sparql_prefixes()}
    
    select ?ev ?round ?gp_name ?score ?team_name 
    
    where {{
      ?ev a fau-f1:Formula1GrandPrix ;
          fau-f1:isInYear ?year ;
          fau-f1:isGpRound ?round ;
          fau-ev:isEventOf ?gp .
      
      ?gp skos:prefLabel ?gp_name .
      
      ?ev_score a fau-f1:FantasyEventScore ;
                fau-f1:isForEvent ?ev ;
                fau-f1:hasEventScore ?score ;
                fau-f1:isForTeam ?team .
          
      ?team foaf:name ?team_name .  
      
      filter (?year = {season.n3()}) }}
      
      ORDER BY ?round
    """


def teams_and_members():
    return f"""
    {sparql_prefixes()}

    select ?team_name ?member_name 

    where {{
    ?team a fau-f1:FantasyTeam ;
          foaf:name ?team_name ;
          fau-f1:hasFantasyMembers ?member .
    
      ?member foaf:name ?member_name .
    }}
    ORDER BY ?team_name
    """

