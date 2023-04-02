from typing import List, Tuple, Dict
from rdflib import Graph
from functools import reduce
from dataclasses import dataclass

from f1fantasy import model, query, dataframe
from f1fantasy.util import fn


def team_scores(g: Graph, season: int, accum: bool, sort: bool = False):
    scores = _scores_table(_team_scores_query(g, season))

    if not accum:
        return dataframe.build_df(scores, sort)

    acc_scores = _accumulate_scores(scores)


    return dataframe.build_df(acc_scores, sort)


def _team_scores_query(g: Graph, season: int) -> List[model.FantasyTeamEventScore]:
    return query.team_scores_by_gp_event(g, season)


def _scores_table(scores: List[model.FantasyTeamEventScore]):
    score_tuples = _scores_to_tuples(scores)
    return reduce(_reducer, score_tuples, _empty_table(score_tuples))


def _empty_table(score_tuples: List[Tuple]) -> Dict:
    """
    Takes in scores generated from a SPARQL query which have been converted to a list of tuples
        [('BAH', 1, 'Bellasi Bronzino', 49), ('BAH', 1, 'Clojos', 212),('SAU', 2, 'Bellasi Bronzino', 186), ('SAU', 2, 'Clojos', 183)]
    Finds all the events to be used for the column headings > {('SAU', 2), ('BAH', 1)}
    Finally returns a Dict as follows > {'team': [], '1-BAH': [], '2-SAU': []}
    :param score_tuples:
    :return:
    """
    sorted({(score[0], score[1]) for score in score_tuples}, key=lambda s: s[1])
    table = {"team": []}
    [table.update({f"{rd}-{ev}": []}) for ev, rd in
     sorted({(score[0], score[1]) for score in score_tuples}, key=lambda s: s[1])]
    return table


def _reducer(table: Dict, row):
    ev, rd, team, points = row
    if team not in table['team']:
        table['team'].append(team)
    column_name = [k for k in table.keys() if str(rd) in k][0]
    table[column_name].append(points)
    return table


def _accumulate_scores(scores: Dict):
    _teams, all_races = fn.fst_rst(list(scores.keys()))
    if not all_races:
        return scores

    fst_race, *races = all_races
    return {**{"team": scores['team']}, **acc_for_round(scores, {fst_race: scores[fst_race]}, fst_race, races)}


def acc_for_round(scores, accums, loc_of_last_accum, races):
    this_race, nxt_races = fn.fst_rst(list(races))
    if not this_race:
        return accums
    accums.update({this_race: [x + y for x, y in zip(accums[loc_of_last_accum], scores[this_race])]})
    if not nxt_races:
        return accums
    return acc_for_round(scores, accums, this_race, nxt_races)


def _scores_to_tuples(scores: List[model.FantasyTeamEventScore]) -> List[Tuple]:
    team_scores = [(score.for_event.gp.symbolic_name,
                    score.for_event.for_round,
                    score.for_team.name,
                    score.points) for score in scores]
    return sorted(team_scores, key=lambda s: s[1])
