from rdflib import Literal

def gp_by_symbol_query(gp_symbol: str):
    return f"""
    select ?gp ?gp_name ?label 

    where {{
    ?gp a fau-f1:GrandPrix ;
          fau-f1:hasSymbol {Literal(gp_symbol).n3()} ;
          fau-f1:gpName ?gp_name ; 
          skos:prefLabel ?label .
    }}
    """

def season_by_year_query(year: int):
    return f"""
    select ?season 

    where {{
    ?season a fau-f1:Season ;
          fau-f1:forYear {Literal(year).n3()} .
    }}
    """


