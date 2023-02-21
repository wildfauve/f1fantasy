from typing import Tuple, Dict
from pymonad.reader import Pipe

from f1fantasy import domain, query, model

from . import helpers, commanda

@commanda.command()
def post_event_fantasy_score(gp_symbol, season_year, team: str, score: int, opts: Dict = None):
    result, _, _ = (Pipe((model.Result.OK, helpers.graph(), (gp_symbol, season_year, team, score)))
                    .then(_fantasy_score_model)
                    .then(_build_score_triples)
                    .flush())
    return result


def _fantasy_score_model(val: Tuple) -> Tuple:
    _, g, (gp_symbol, season_year, team, score) = val

    ev = query.find_gp_event_by_symbol_and_season(g, symbol=gp_symbol, season=season_year, to_model=True)
    team = query.find_team_by_name(g, team, to_model=True)

    if not ev:
        return model.Result.ERR, g, f"Cant find Event for GP {gp_symbol}"
    if not team:
        return model.Result.ERR, g, f"Cant find Team with name {team}"

    return model.Result.OK, g, model.FantasyTeamEventScore(for_team=team, for_event=ev, points=score)


def _build_score_triples(val: Tuple) -> Tuple:
    result, g, team_score_model = val
    if result == model.Result.ERR:
        return val
    domain.post_event_score(g, team_score_model)
    return model.Result.OK, g, team_score_model
