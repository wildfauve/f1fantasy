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
