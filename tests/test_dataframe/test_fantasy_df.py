import polars as pl

from f1fantasy import dataframe, repo


def test_generate_season_scores(configure_repo,
                                season_2023,
                                create_gp_for_bah,
                                create_gp_for_sau,
                                bah_event,
                                sau_event,
                                team_clojos,
                                team_lighthouse,
                                team_scores_multi_event):
    df = dataframe.team_scores(repo.graph(), 2023)

    series = df.select(pl.all()).to_dict()

    assert series['team'].to_list() == ['Clojos', 'LightHouse']
    assert series['1-BAH'].to_list() == [100, 120]
    assert series['2-SAU'].to_list() == [150, 220]
