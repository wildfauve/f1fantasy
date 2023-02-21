from typing import List, Tuple, Dict
import polars as pl
from rdflib import Graph
from functools import reduce

from f1fantasy import model, query


def team_scores(g: Graph, season: int) -> pl.DataFrame:
    scores = _scores_table(_team_scores_query(g, season))

    return pl.DataFrame(scores)


def _team_scores_query(g: Graph, season: int) -> List[model.FantasyTeamEventScore]:
    return query.team_scores_by_gp_event(g, season)


def _scores_table(scores: List[model.FantasyTeamEventScore]):
    score_tuples = _scores_to_tuples(scores)
    return reduce(_reducer, score_tuples, _empty_table(score_tuples))


def _empty_table(score_tuples: List[Tuple]) -> Dict:
    sorted({(score[0], score[1]) for score in score_tuples}, key=lambda s: s[1])
    table = {"team": []}
    [table.update({f"{rd}-{ev}": []}) for ev, rd in sorted({(score[0], score[1]) for score in score_tuples}, key=lambda s: s[1])]
    return table


def _reducer(table: Dict, row):
    ev, rd, team, points = row
    if team not in table['team']:
        table['team'].append(team)
    column_name = [k for k in table.keys() if str(rd) in k][0]
    table[column_name].append(points)
    return table


def _scores_to_tuples(scores: List[model.FantasyTeamEventScore]) -> List[Tuple]:
    team_scores = [(score.for_event.gp.symbolic_name,
                    score.for_event.for_round,
                    score.for_team.name,
                    score.points) for score in scores]
    return sorted(team_scores, key=lambda s: s[1])
