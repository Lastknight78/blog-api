import random
from enum import Enum


class BaseEnum(Enum):
    @classmethod
    def random(cls):
        return random.choice(list(cls))
