Genetic Algorithms for python
==============

This library hopes to build a wrapper for genetic algorithms to leverage in optimisation situations.
It hopes to make writing infinitely customizable genetic algorithms easy and quick while having all the standard features expected.

Examples
--------
This is a basic example for maximising values in a list, starring with 10 members running 100 generation.
Then it will log to the screen and create a csv file with each generations information.

    >>>import src as ga
    >>>class MyMember(ga.MemberBase):
    >>>   def _construct_from_params(self, construction_parameters=None):
    >>>       self.vars = [random.randrange(10) for _ in range(5)]
    >>>
    >>>   def mutate(self):
    >>>       # i = random.randrange(len(self.vars))
    >>>       j = random.randrange(len(self.vars))
    >>>       # tmp = self.vars[i]
    >>>       # self.vars[i] = self.vars[j]
    >>>       self.vars[j] += 1
    >>>
    >>>   def crossover(self, pairing):
    >>>       new_params = self.vars[:len(self.vars) // 2] + pairing.vars[len(pairing.vars) // 2:]
    >>>       return MyMember(new_params)
    >>>
    >>>   def score_self(self):
    >>>       return sum(self.vars)
    >>>
    >>> def m_fit_func(member: MyMember):
    >>>     return member.score_self()
    >>>
    >>> pop = ga.Population(size=10, member_type=MyMember, member_parameters_generator=None,
    >>>                   fitness_function=m_fit_func, population_seed=0)
    >>> pop.run(100, print_logging=True, csv_path="example1.csv")


