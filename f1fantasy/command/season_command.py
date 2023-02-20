from typing import Tuple
from pymonad.reader import Pipe

from f1fantasy import domain, query, model

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


def create_season_event(gp_symbol, season_year, gp_date: str, for_round: int):
    result, _, _ = (Pipe((model.Result.OK, helpers.graph(), (gp_symbol, season_year, gp_date, for_round)))
                    .then(_gp_event_model)
                    .then(_build_gp_event_triples)
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


def _build_gp_triples(val: Tuple) -> Tuple:
    _, g, gp_model = val
    domain.add_gp(g, gp_model)
    return model.Result.OK, g, gp_model


def _gp_event_model(val: Tuple) -> Tuple:
    _, g, (gp_symbol, season_year, gp_date, for_round) = val

    gp = query.find_gp_by_symbol(g, gp_symbol, to_model=True)
    yr = query.find_season_by_year(g, season_year, to_model=True)

    if not gp:
        return model.Result.ERR, g, f"Cant find GP with symbol {gp_symbol}"

    return model.Result.OK, g, model.GpEvent(gp=gp,
                                             season=yr,
                                             round=for_round,
                                             gp_date=gp_date)


def _build_gp_event_triples(val: Tuple) -> Tuple:
    _, g, gp_event_model = val
    domain.add_gp_event(g, gp_event_model)
    return model.Result.OK, g, gp_event_model
