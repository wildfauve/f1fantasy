from typing import Tuple
from pymonad.reader import Pipe

from f1fantasy import domain
from f1fantasy import model
from f1fantasy import repo

from . import helpers

def create_season(season: int):
    result, _, _ = (Pipe((model.Result.OK, helpers.graph(), season))
                    .then(_season_model)
                    .then(_build_season_triples)
                    .then(helpers.save)
                    .flush())
    return result


def create_gp(name, symbol, label):
    result, _, _ = (Pipe((model.Result.OK, helpers.graph(), (name, symbol, label)))
                    .then(_gp_model)
                    .then(_build_gp_triples)
                    .then(helpers.save)
                    .flush())
    return result


def _season_model(val: Tuple) -> Tuple:
    _, g, season = val
    return model.Result.OK, g, model.Season(season)


def _build_season_triples(val: Tuple) -> Tuple:
    _, g, season = val
    domain.add_season(g, season)
    return model.Result.OK, g, season


def _gp_model(val: Tuple) -> Tuple:
    _, g, (name, symbol, label) = val
    return model.Result.OK, g, model.Gp(name=name, symbolic_name=symbol, label=label)
    breakpoint()


def _build_gp_triples(val: Tuple) -> Tuple:
    _, g, gp_model = val
    domain.add_gp(g, gp_model)
    return model.Result.OK, g, gp_model
