import random
import unittest

import genetic_algorithms as ga


class PopulationTests(unittest.TestCase):
    def test_creation_basic(self):
        class MyMember(ga.MemberBase):
            def _construct_from_params(self, construction_parameters=None):
                self.vars = [random.randrange(10) for _ in range(10)]

            # Create mutate and score are not needed for creation
            def mutate(self):
                pass

            def crossover(self, pairing):
                pass

            def score_self(self):
                pass

        pop = ga.Population(10, MyMember, MyMember.score_self)
        self.assertEqual(len(pop.population), 10)
        self.assertEqual(pop.member_type, MyMember)
        self.assertEqual(pop.fitness_function, MyMember.score_self)

    def test_creation_custom_fitness(self):
        class MyMember(ga.MemberBase):
            def _construct_from_params(self, construction_parameters=None):
                self.vars = [random.randrange(10) for _ in range(10)]

            # Create mutate and score are not needed for creation
            def mutate(self):
                pass

            def crossover(self, pairing):
                pass

        def custom_fit_func():
            pass

        pop = ga.Population(10, MyMember, custom_fit_func)
        self.assertEqual(len(pop.population), 10)
        self.assertEqual(pop.member_type, MyMember)
        self.assertEqual(pop.fitness_function, custom_fit_func)


if __name__ == '__main__':
    unittest.main()
