from typing import Optional
from f1fantasy.f1_seasons import competition
from f1fantasy.fantasy import teams

def display_teams():
    teams.show(generate_graph())
