from f1fantasy import query, repo
def test_generate_season_scores(configure_repo,
                                season_2023,
                                create_gp_for_bah,
                                bah_event,
                                team_clojos,
                                team_lighthouse,
                                team_scores_single_event):
    result = query.team_scores_by_gp_event(repo.graph(), 2023)

    rows = [(score.for_event.gp.symbolic_name, score.for_team.name, score.points) for score in result]

    expected = [('BAH', 'Clojos', 100), ('BAH', 'LightHouse', 120)]

    assert rows == expected
