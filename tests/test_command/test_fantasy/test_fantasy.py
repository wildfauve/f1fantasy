from rdflib import Literal, RDF, URIRef

from f1fantasy import command, model, rdf, repo


def test_post_score(configure_repo, season_2023, create_gp_for_bah, bah_event, team_clojos):
    result = command.post_event_fantasy_score(gp_symbol="BAH", season_year=2023, team="Clojos", score=100)

    assert result == model.Result.OK

    team_score = rdf.all_matching_triples(repo.graph(), (
    URIRef('https://fauve.io/fantasyTeam/Clojos/EventScore/BAH-2023'), None, None))

    expected_objs = {'https://fauve.io/ontology/F1/FantasyEventScore', 'https://fauve.io/f1/grandPrix/2023/BAH', 100,
                     'https://fauve.io/fantasyTeam/Clojos'}

    assert {r[2].toPython() for r in team_score} == expected_objs

