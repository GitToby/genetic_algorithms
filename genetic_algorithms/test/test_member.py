import unittest
import genetic_algorithms as ga


class PopulationTests(unittest.TestCase):
    def test_is_abstract_errors(self):
        member = ga.MemberBase
        self.assertRaises(NotImplementedError, member._construct_from_params, None)
        self.assertRaises(NotImplementedError, member.mutate, None)
        self.assertRaises(NotImplementedError, member.crossover, None, None)

    def test_seeding(self):
        pass