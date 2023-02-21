from typing import Tuple

from f1fantasy import repo

def save(val: Tuple = None) -> Tuple:
    repo.save()
    return val


def graph():
    return repo.graph()
