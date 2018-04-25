import random


class MemberBase(object):
    def __init__(self,
                 construction_parameters=None,
                 seed=None) -> None:
        super().__init__()
        self.construction_parameters = construction_parameters
        self.member_type = type(self)
        self.seed = seed
        if seed is not None:
            random.seed(seed)

        self._construct_from_params(self.construction_parameters)

    def _construct_from_params(self, construction_parameters=None):
        raise NotImplementedError('Default MemberBase cannot be constructed. Extend this class to build a GA')

    def mutate(self):
        raise NotImplementedError('Default MemberBase cannot be mutated. Extend this class to build a GA')

    def crossover(self, pairing):
        raise NotImplementedError('Default MemberBase cannot be mutated. Extend this class to build a GA')
