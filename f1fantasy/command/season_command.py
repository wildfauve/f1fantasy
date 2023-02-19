from typing import Tuple
from pymonad.reader import Pipe

from f1fantasy import domain
from f1fantasy import model
from f1fantasy import repo


def create_season(season: int):
    result, _, _ = (Pipe((model.Result.OK, _graph(), season))
                    .then(_season_model)
                    .then(_build_triples)
                    .then(_save)
                    .flush())
    return result

def _season_model(val: Tuple) -> Tuple:
    _, g, season = val
    return model.Result.OK, g, model.Season(season)


def _build_triples(val: Tuple) -> Tuple:
    _, g, season = val
    domain.add_season(g, season)
    return model.Result.OK, g, season


def _save(val: Tuple) -> Tuple:
    repo.save()
    return val


def _graph():
    return repo.graph()
