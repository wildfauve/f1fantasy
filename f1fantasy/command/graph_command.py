from typing import Optional
from f1fantasy.f1_seasons import competition
from f1fantasy.fantasy import teams

def generate_graph(season: Optional[int] = None):
    return competition.build(season)

def display_teams():
    teams.show(generate_graph())
