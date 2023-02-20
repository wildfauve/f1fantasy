from rdflib import Literal, RDF
from f1fantasy import rdf

def post_event_score(g, score):
    g.add((score.subject, RDF.type, rdf.P.fau_f1.FantasyEventScore))
    g.add((score.subject, rdf.P.fau_f1.isForTeam, score.for_team.subject))
    g.add((score.subject, rdf.P.fau_f1.isForEvent, score.for_event.subject))
    g.set((score.subject, rdf.P.fau_f1.hasEventScore, Literal(score.points)))
    return g

