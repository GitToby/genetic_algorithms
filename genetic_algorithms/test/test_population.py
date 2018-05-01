import unittest
from genetic_algorithms.test.members_util import *


class PopulationTests(unittest.TestCase):
    def test_creation_basic(self):
        pop = ga.Population(10, MyMemberEmpty, MyMemberEmpty.score_self)
        self.assertEqual(len(pop.population), 10)
        self.assertEqual(pop.member_type, MyMemberEmpty)
        self.assertEqual(pop.fitness_function, MyMemberEmpty.score_self)

    def test_population_fitness_minimise(self):
        def custom_fit_func(member):
            return sum(member.vars)

        pop = ga.Population(10, MyMemberIntList, custom_fit_func)
        start_scores = sum([custom_fit_func(x) for x in pop.population])
        pop.run(50, maximise_fitness_func=False)
        end_scores = sum([custom_fit_func(x) for x in pop.population])
        self.assertTrue(end_scores <= start_scores)

    def test_population_fitness_maximise(self):
        def custom_fit_func(member):
            return sum(member.vars)

        pop = ga.Population(10, MyMemberIntList, custom_fit_func)
        start_scores = sum([custom_fit_func(x) for x in pop.population])
        pop.run(50, maximise_fitness_func=True)
        end_scores = sum([custom_fit_func(x) for x in pop.population])
        self.assertTrue(end_scores >= start_scores)

    def test_size_error(self):
        self.assertRaises(ValueError, ga.Population, -1, MyMemberEmpty, None)
        self.assertRaises(ValueError, ga.Population, 0, MyMemberEmpty, None)

    def test_population_pass(self):
        def custom_fit_func(member):
            return sum(member.vars)

        pre_made_population = [MyMemberIntList() for _ in range(10)]
        pop = ga.Population(10, MyMemberIntList, custom_fit_func, population=pre_made_population)
        self.assertListEqual(pop.population, pre_made_population)

    def test_get_top_member(self):
        pop = ga.Population(10, MyMemberIntList, None)
        self.assertEqual(pop.get_top_member(include_fitness=False), pop.population[0])

    def test_get_top_member_with_fitness(self):
        def custom_fit_func(member):
            return sum(member.vars)

        pop = ga.Population(10, MyMemberIntList, custom_fit_func)
        self.assertEqual(pop.get_top_member(include_fitness=True), (pop.population[0], 52))

    def test_print_logging(self):
        pass

    def test_to_csv(self):
        pass
