from rdflib import Literal, RDF, URIRef

from f1fantasy import command, model, rdf, repo


def test_rank_plot(configure_repo,
                   season_2023,
                   create_gp_for_bah,
                   create_gp_for_sau,
                   bah_event,
                   sau_event,
                   team_clojos,
                   team_lighthouse):
    command.post_points_file(file='tests/fixtures/load_points_acc_bah_2023.csv', season=2023, accum=True)
    command.post_points_file(file='tests/fixtures/load_points_acc_sau_2023.csv', season=2023, accum=True)

    command.scores_plot(2023)


