import pytest
from pathlib import Path

from f1fantasy.repo import triples

BASE_PATH = (Path(__file__).parent.parent / "fixtures" / "f1fantasy-model.ttl")

@pytest.fixture
def init_repo():
    triples.Repo().configure(triples_location=BASE_PATH)
    yield
    triples.drop()

@pytest.fixture
def empty_graph():
    return triples.graph()