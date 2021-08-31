import numpy as np
import random

import genetic_algorithms as ga


# Example 1 - Very basic, lets maximise the sum of the variables.
class MyMember(ga.MemberBase):
    def _construct_from_params(self, construction_parameters=None):
        self.vars = [random.randrange(10) for _ in range(5)]

    def mutate(self):
        # i = random.randrange(len(self.vars))
        j = random.randrange(len(self.vars))
        # tmp = self.vars[i]
        # self.vars[i] = self.vars[j]
        self.vars[j] += 1

    def crossover(self, pairing):
        new_params = self.vars[:len(self.vars) // 2] + pairing.vars[len(pairing.vars) // 2:]
        return MyMember(new_params)

    def score_self(self):
        return sum(self.vars)


def m_fit_func(member: MyMember):
    return member.score_self()


pop = ga.Population(size=10, member_type=MyMember, member_parameters_generator=None,
                    fitness_function=m_fit_func, population_seed=0)
pop.run(100, print_logging=True, csv_path="example1.csv")
