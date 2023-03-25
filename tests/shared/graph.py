import pytest
from pathlib import Path

from f1fantasy import command, repo

BASE_PATH = (Path(__file__).parent.parent / "fixtures" / "db_test.ttl")


@pytest.fixture
def configure_repo():
    repo.RepoContext().configure(triples_location=BASE_PATH)
    repo.init()
    yield
    repo.drop()


@pytest.fixture
def empty_graph():
    return repo.triples.graph()


@pytest.fixture
def season_2023():
    command.create_season(2023)


@pytest.fixture
def create_gp_for_bah():
    command.create_gp('Bahrain Grand Prix', 'BAH', "Bahrain")


@pytest.fixture
def create_gp_for_sau():
    command.create_gp('Saudi Arabian Grand Prix', 'SAU', "SaudiArabia")


@pytest.fixture
def bah_event():
    command.create_season_event(gp_symbol="BAH", season_year=2023, gp_date='2023-03-05', for_round=1)


@pytest.fixture
def sau_event():
    command.create_season_event(gp_symbol="SAU", season_year=2023, gp_date='2023-03-10', for_round=2)


@pytest.fixture
def team_clojos():
    command.create_team("Clojos", ("Claudie", "Fyodoro"), "Perky")


@pytest.fixture
def team_lighthouse():
    command.create_team("LightHouse", ("Florence", "Piri"), "Perky")


@pytest.fixture
def team_scores_single_event():
    (command.runner()
     .cmd(command._post_event_fantasy_score, "BAH", 2023, team="Clojos", score=100)
     .cmd(command._post_event_fantasy_score, "BAH", 2023, "LightHouse", 120)
     .run())


@pytest.fixture
def team_scores_multi_event():
    (command.runner()
     .cmd(command._post_event_fantasy_score, "BAH", 2023, team="Clojos", score=100)
     .cmd(command._post_event_fantasy_score, "BAH", 2023, "LightHouse", 120)
     .cmd(command._post_event_fantasy_score, "SAU", 2023, team="Clojos", score=150)
     .cmd(command._post_event_fantasy_score, "SAU", 2023, "LightHouse", 220)
     .run())
