from typing import List

from f1fantasy import query
from f1fantasy import repo


def seasons() -> List[str]:
    return [str(season) for season in query.all_seasons(repo.graph())]

def gp_symbols() -> List[str]:
    return [symb for symb in query.all_gps(repo.graph())]

def team_names() -> List[str]:
    result = query.all_teams(repo.graph(), to_model=True)
    return [team.name for team in result]
