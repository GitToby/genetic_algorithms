import genetic_algorithms as ga
import random


class MyMemberEmpty(ga.MemberBase):
    def _construct_from_params(self, construction_parameters=None):
        self.vars = [random.randrange(10) for _ in range(10)]

    # Create mutate and score are not needed for creation
    def mutate(self):
        pass

    def crossover(self, pairing):
        pass

    def score_self(self):
        pass


class MyMemberIntList(ga.MemberBase):
    def _construct_from_params(self, construction_parameters=None):
        self.vars = [random.randrange(10) for _ in range(10)]

    def mutate(self):
        pos = random.randrange(len(self.vars))
        self.vars[pos] -= 1

    def crossover(self, pairing):
        new_vars = self.vars[:len(self.vars)] + pairing.vars[len(pairing.vars):]
        return self.member_type(new_vars)
