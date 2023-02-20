from typing import List

from f1fantasy import query
from f1fantasy import repo


def seasons() -> List[str]:
    return [str(season) for season in query.all_seasons(repo.graph())]

def gp_symbols() -> List[str]:
    return [symb for symb in query.all_gps(repo.graph())]
