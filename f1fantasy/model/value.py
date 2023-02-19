from dataclasses import dataclass
from enum import Enum

class Result(Enum):
    OK = 'ok'
    ERR = 'err'

@dataclass
class ValueObject:
    def replace(self, key, value):
        setattr(self, key, value)
        return self
