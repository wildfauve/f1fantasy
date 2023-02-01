import pytest

from f1fantasy.repo import triples


@pytest.fixture
def empty_graph():
    return triples.graph()