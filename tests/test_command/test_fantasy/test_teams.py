from rdflib import Literal, RDF

from f1fantasy import command
from f1fantasy import model
from f1fantasy import rdf
from f1fantasy import repo


def test_create_team(configure_repo):
    result = command.create_team("Clojos", ("Claudie", "Fyodoro"), "Perky")

    assert result == model.Result.OK

    teams = list(rdf.all_matching_triples(repo.graph(), (None, RDF.type, rdf.P.fau_f1.FantasyTeam)))

    assert len(teams) == 1

    _, _, team_name = rdf.first_matching_triple(repo.graph(), (teams[0][0], rdf.P.foaf.name, None))

    assert team_name.toPython() == "Clojos"

    members = {name.toPython() for name in member_names_for_team(repo.graph(), teams[0][0])}

    assert members == {'Claudie', 'Fyodoro'}

def member_names_for_team(g, team_sub):
    return [mem_name(g, mem_sub) for _, _, mem_sub in
            rdf.all_matching_triples(g, (team_sub, rdf.P.fau_f1.hasFantasyMembers, None))]


def mem_name(g, sub):
    _, _, member_name = rdf.first_matching_triple(repo.graph(), (sub, rdf.P.foaf.name, None))
    return member_name
