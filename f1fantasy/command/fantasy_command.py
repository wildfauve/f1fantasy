from typing import Tuple, Dict, Callable
from pymonad.reader import Pipe
from functools import partial

from f1fantasy import domain, query, model, repo, dataframe

from . import helpers, commanda


@commanda.command()
def post_event_fantasy_score(gp_symbol, season_year, team: str, score: int, opts: Dict = None):
    g = helpers.graph()
    result, _, _, _ = (
        Pipe((model.Result.OK, g, team_scores_query(season_year, True, g), (gp_symbol, season_year, team, score)))
        .then(partial(_fantasy_score_model, model.event_score_per_race))
        .then(_build_score_triples)
        .flush())
    return result


@commanda.command()
def post_event_fantasy_accum_score(gp_symbol, season_year, team: str, score: int, opts: Dict = None):
    g = helpers.graph()
    result, _, _, _ = (
        Pipe((model.Result.OK, g, team_scores_query(season_year, True, g), (gp_symbol, season_year, team, score)))
        .then(partial(_fantasy_score_model, model.event_score_from_aggregate))
        .then(_build_score_triples)
        .flush())
    return result


def team_scores_query(season: int, accum: bool, g=None):
    return dataframe.team_scores(g=g if g else repo.graph(), season=int(season), accum=accum)


def _fantasy_score_model(event_score_fn: Callable, val: Tuple) -> Tuple:
    _, g, df, (gp_symbol, season_year, team, score) = val

    ev = query.find_gp_event_by_symbol_and_season(g, symbol=gp_symbol, season=season_year, to_model=True)
    team = query.find_team_by_name(g, team, to_model=True)

    if not ev:
        return model.Result.ERR, g, f"Cant find Event for GP {gp_symbol}"
    if not team:
        return model.Result.ERR, g, f"Cant find Team with name {team}"

    return model.Result.OK, g, df, event_score_fn(for_team=team, for_event=ev, points=score, df=df)


def _build_score_triples(val: Tuple) -> Tuple:
    result, g, df, team_score_model = val
    if result == model.Result.ERR:
        return val
    domain.post_event_score(g, team_score_model)
    return model.Result.OK, g, df, team_score_model
