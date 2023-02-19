from f1fantasy.model import fantasy
from ...domain import teams
from . import events


scores = [
    fantasy.FantasyTeamEventScore(for_event=events.BahrainGrandPrix_2023, for_team=teams.TeamClojos, points=100)
]
