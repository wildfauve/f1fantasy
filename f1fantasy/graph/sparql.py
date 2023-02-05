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

def team_scores_by_gp_event(year: Literal):
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
      
      filter (?year = {year.n3()}) }}
      
      ORDER BY ?round
    """


def positions_by_navdatetime(navdatetime: Literal) -> str:
    """
    This query takes a NAVDateTime and finds all the subjects which are mandatory for that time.

    Every Portfolio has:
    + a constituent; the holding.
    + a position valuation for that constituent.
    + a position valuation change for that constituent.
    + a cost valuation change for that constituent.

    Note: Don't query for any triples that are optional for any element of the triple.
    Otherwise ths query will return zero rows.

    :param navdatetime:
    :return:
    """
    return """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
    prefix fibo-fnd-arr-arr: <https://spec.edmcouncil.org/fibo/ontology/FND/Arrangements/Arrangements/>
    prefix fibo-fnd-oac-own: <https://spec.edmcouncil.org/fibo/ontology/FND/OwnershipAndControl/Ownership/>
    prefix fibo-sec-fund-civ: <https://spec.edmcouncil.org/fibo/ontology/SEC/Funds/CollectiveInvestmentVehicles/>
    prefix sfo-prt: <https://nzsuperfund.co.nz/ontology/PRT/>
    
    select distinct ?portfolio ?constituent ?posvaluation ?navdateval ?posvaluationchange ?navdatevalchg ?costvaluation ?navdatecost ?fi
    
    where {{
          ?portfolio a fibo-sec-fund-civ:FundPortfolio ;
             fibo-fnd-arr-arr:hasConstituent ?constituent .
        
          ?constituent sfo-prt:hasPosition ?posvaluation ;
                       sfo-prt:hasCostValuation ?costvaluation ;
                       sfo-prt:hasPositionValuationChange ?posvaluationchange .
                 
          ?costvaluation sfo-prt:hasNAVDateTime ?navdatecost .
      
          ?posvaluationchange sfo-prt:hasNAVDateTime ?navdatevalchg .
      
          ?posvaluation sfo-prt:hasNAVDateTime ?navdateval . 
      
          ?const a ?const_type ;
                 fibo-fnd-oac-own:hasOwnedAsset ?fi .
          
          filter (?navdateval = {navdt} &&
                 ?navdatevalchg = {navdt} &&
                 ?navdatecost = {navdt})
    }}    
    """.format(navdt=navdatetime.n3())


def portfolio_navdate_group_by():
    return """
    prefix fibo-fnd-arr-rt: <https://spec.edmcouncil.org/fibo/ontology/FND/Arrangements/Ratings/>
    prefix fibo-fnd-oac-own: <https://spec.edmcouncil.org/fibo/ontology/FND/OwnershipAndControl/Ownership/>
    prefix fibo-sec-fund-civ: <https://spec.edmcouncil.org/fibo/ontology/SEC/Funds/CollectiveInvestmentVehicles/>
    prefix sfo-prt: <https://nzsuperfund.co.nz/ontology/PRT/>
    
    select ?navdatetime  (sample(?port) as ?portfolio)
                         (sample(?const) as ?constituent)
                         (sample(?posval) as ?positionval)
                         (sample(?posvalchg) as ?positionvalchg)
                         (sample(?costval) as ?costvaluation)
                         (sample(?fi) as ?instrument)
    
    where {
          ?port a fibo-sec-fund-civ:FundPortfolio ;
             fibo-fnd-arr-arr:hasConstituent ?holding .
    
          ?const sfo-prt:hasPosition ?posval ;
                 sfo-prt:hasCostValuation ?costval ;
                 sfo-prt:hasPositionValuationChange ?posvalchg .
    
          ?posval sfo-prt:hasNAVDateTime ?navdatetime .
    
          ?const a ?const_type ;
                 fibo-fnd-oac-own:hasOwnedAsset ?fi .
    
    }
    
    group by ?navdatetime
    """
