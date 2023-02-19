import pytest
from pathlib import Path

from f1fantasy import repo

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