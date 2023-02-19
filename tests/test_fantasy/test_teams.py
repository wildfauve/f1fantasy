from rdflib import RDF

from f1fantasy.domain import teams
from f1fantasy.repo import triples
from f1fantasy.rdf import gn


def test_add_teams_to_graph(configure_repo, empty_graph):
    g = triples.save(teams.teams(empty_graph))

    team_triples = gn.all_matching_triples(g, (None, RDF.type, rdf_prefix.fau_f1.FantasyTeam))

    expected_subjects = {'https://fauve.io/fantasyTeam/TeamClojo', 'https://fauve.io/fantasyTeam/TeamFauve',
                         'https://fauve.io/fantasyTeam/TeamGelatoGiants', 'https://fauve.io/fantasyTeam/TeamLightHouse',
                         'https://fauve.io/fantasyTeam/TeamMusicalBears'}

    teams_subjects = {s.toPython() for s, _, _ in team_triples}

    assert teams_subjects == expected_subjects


def test_idempotent_teams_add(configure_repo, empty_graph):
    g = triples.save(teams.teams(empty_graph))

    g = triples.save((teams.teams(g)))

    team_triples = gn.all_matching_triples(g, (None, RDF.type, rdf_prefix.fau_f1.FantasyTeam))

    expected_subjects = {'https://fauve.io/fantasyTeam/TeamClojo', 'https://fauve.io/fantasyTeam/TeamFauve',
                         'https://fauve.io/fantasyTeam/TeamGelatoGiants', 'https://fauve.io/fantasyTeam/TeamLightHouse',
                         'https://fauve.io/fantasyTeam/TeamMusicalBears'}

    teams_subjects = {s.toPython() for s, _, _ in team_triples}

    assert teams_subjects == expected_subjects


def test_display_teams(capsys, configure_repo, empty_graph):
    g = triples.save(teams.teams(empty_graph))

    teams.show(g)

    captured = capsys.readouterr()

    expected = """Clojos
|__ Claudie
|__ Fyodoro"""

    assert expected in captured.out