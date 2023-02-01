from dataclasses import dataclass

@dataclass
class ValueObject:
    def replace(self, key, value):
        setattr(self, key, value)
        return self
