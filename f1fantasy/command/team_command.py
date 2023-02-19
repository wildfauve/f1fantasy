from typing import Optional, Tuple
from pymonad.reader import Pipe

from f1fantasy import domain, model

from . import helpers


def create_team(team_name: str, members: Tuple[str], manager: str):
    result, _, _ = (Pipe((model.Result.OK, helpers.graph(), (team_name, members, manager)))
                    .then(_team_model)
                    .then(_build_triples)
                    .then(helpers.save)
                    .flush())
    return result


def _team_model(val: Tuple) -> Tuple:
    _, g, (team_name, team_members, manager) = val
    team_model = model.FantasyTeam(name=team_name,
                                   manager=model.Member(name=manager).subject,
                                   members=[model.Member(name=member) for member in team_members])
    return model.Result.OK, g, team_model


def _build_triples(val: Tuple) -> Tuple:
    _, g, team_model = val
    domain.add_teams_to_graph(g, team_model)
    return model.Result.OK, g, team_model
