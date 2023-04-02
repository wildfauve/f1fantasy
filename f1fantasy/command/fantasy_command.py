from typing import Tuple, Dict, Callable
from pymonad.reader import Pipe
from functools import partial
import csv

from f1fantasy import domain, query, model, repo, plot
from f1fantasy.initialiser import rich

from . import helpers, commanda, fantasy_df_builder


@commanda.command()
def post_points_file(file: str, season: int, accum: bool = False):
    g = helpers.graph()
    df = team_scores_query(season, False, g)
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for gp_symbol, team, points in reader:
            rich.console.print(f"gp: [blue]{gp_symbol}, team: [yellow]{team}, points: [green]{points}")
            post_runner(model.event_score_from_aggregate if accum else model.event_score_per_race,
                        g,
                        df,
                        gp_symbol,
                        season,
                        team,
                        int(points))

    return model.Result.OK

@commanda.command()
def post_score_controller(gp_symbol, season_year, team: str, score: int, accum: bool = False, opts: Dict = None):
    g = helpers.graph()
    df = team_scores_query(season_year, True, g)
    return post_runner(model.event_score_from_aggregate if accum else model.event_score_per_race,
                       g,
                       df,
                       gp_symbol,
                       season_year,
                       team,
                       score)


def post_runner(points_fn, g, df, gp_symbol, season_year, team, score):
    result, _, _, _ = (
        Pipe((model.Result.OK, g, df, (gp_symbol, season_year, team, score)))
        .then(partial(_fantasy_score_model, points_fn))
        .then(_build_score_triples)
        .flush())
    return result


def team_scores_query(season: int, accum: bool, g=None):
    return fantasy_df_builder.team_scores(g=g if g else repo.graph(), season=int(season), accum=accum)


def scores_plot(file: str, season: int, g=None):
    df = team_scores_query(season, True, g)
    return plot.rank_plot(file, df)



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
