import random
import unittest
import numpy as np
from itertools import starmap

import src as ga


class EndToEndTests(unittest.TestCase):
    def test_e2e_basic(self):
        class MyMember(ga.MemberBase):
            def _construct_from_params(self, construction_parameters=None):
                self.vars = [random.randrange(10) for _ in range(10)]

            def mutate(self):
                j = random.randrange(len(self.vars))
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
        start_pop = pop.population
        start_scores = list(starmap(m_fit_func, [[m] for m in start_pop]))

        # Ensure good creation
        self.assertEqual(len(pop.population), 10)
        self.assertEqual(pop.member_type, MyMember)
        self.assertEqual(pop.fitness_function, m_fit_func)

        pop.run(10, print_logging=False)
        end_scores = list(starmap(m_fit_func, [[m] for m in pop.population]))
        # Ensure changes have been made
        self.assertNotEqual(pop.population, start_pop)
        self.assertGreaterEqual(max(end_scores), max(start_scores))

    def test_parameter_passing_e2e(self):
        class MyMember(ga.MemberBase):
            def _construct_from_params(self, construction_parameters=None):
                self.height = construction_parameters['height']
                self.width = construction_parameters['width']

            def mutate(self):
                i = random.randrange(2)
                j = random.randrange(2)
                self.height += pow(-1, i)
                self.width += pow(-1, j)

            def crossover(self, pairing):
                new_params = {'height': np.mean([self.height, pairing.height]),
                              'width':  np.mean([self.width, pairing.width])}
                return MyMember(construction_parameters=new_params)

        def fit_through_door(member: MyMember):
            door_height = 10
            door_width = 3
            height_diff = abs(door_height - member.height)
            width_diff = abs(door_width - member.width)
            if height_diff > 0 or width_diff > 0:
                return 1/(height_diff + width_diff)
            else:
                return np.inf

        def param_generator():
            max_h = 10
            max_w = 20
            yield {'height': random.randrange(max_h),
                   'width': random.randrange(max_w)}

        random.seed(1)
        pop = ga.Population(10, MyMember, fit_through_door, member_parameters_generator=param_generator)
        start_pop = pop.population
        self.assertEqual(len(pop.population), 10)
        self.assertEqual(pop.member_type, MyMember)
        self.assertEqual(pop.fitness_function, fit_through_door)
        self.assertDictEqual(pop.population[0].construction_parameters, {'height': 2, 'width': 18})

        # run 5 generations before checking we have some parameters changed
        pop.run(generations=50)
        self.assertEqual(pop.population[0].construction_parameters, {'height': 9.6953125, 'width': 4.1953125})


if __name__ == '__main__':
    unittest.main()
