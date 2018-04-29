from itertools import starmap
import numpy as np
from pandas import DataFrame
import random


class Population(object):
    def __init__(self,
                 size: int,
                 member_type,
                 fitness_function: callable,
                 member_parameters_generator: callable = None,
                 population=None,
                 population_seed=None,
                 member_seed=None) -> None:
        self.member_type = member_type
        self.population = list()
        self.fitness_function = fitness_function
        self.population_seed = population_seed
        self.log_df = DataFrame()
        if self.population_seed is not None:
            random.seed(self.population_seed)

        # check size limits
        if size > 0:
            self.size = size
        else:
            raise ValueError('size must be > 0')

        # Create population on given population or randomly with params from a provided generator.
        # If the generator is None then then nothing will be passed.
        if population is None:
            if member_parameters_generator is None:
                self.population = [self.member_type(seed=member_seed) for _ in range(self.size)]
            else:
                self.population = [self.member_type(construction_parameters=next(member_parameters_generator()),
                                                    seed=member_seed) for _ in range(self.size)]
        else:
            self.population = population

    def get_top(self):
        return self.population[0], self.fitness_function(self.population[0])

    def _get_score_all_zip(self):
        fitness_scores = starmap(self.fitness_function, [[x] for x in self.population])
        member_score_zip = zip(fitness_scores, self.population)
        return member_score_zip

    def _rebuild_population(self):
        # This method can be overridden to customize the rebuilding workflow.
        start_pop = len(self.population)
        missing_pop = self.size - start_pop
        for _ in range(missing_pop):
            i, j = random.randrange(start_pop), random.randrange(start_pop)
            new_member = self.population[i].crossover(self.population[j])
            new_member.mutate()
            # By appending we keep the _known_ best scores at the top.
            self.population.append(new_member)

    def run(self, generations, successful_cutoff: float = 0.4,
            print_logging: bool = False, csv_path: str = None,
            maximise_fitness_func: bool = False) -> None:
        # Indexing from 1
        for gen in range(generations):
            if print_logging:
                print("-----------------------")
                print("Running generation", gen + 1)

            score_list = list(self._get_score_all_zip())

            # sort them in reverse, highest -> smallest score
            score_list = sorted(score_list, key=lambda x: x[0], reverse=maximise_fitness_func)
            (scores, members) = zip(*score_list)

            # remove members below the successful cutoff
            cutoff_point = int(len(score_list) * successful_cutoff)
            self.population = list(members[:cutoff_point])
            self._rebuild_population()

            if print_logging:
                print("Scored members.")
                print("Population score stats:")
                print("| Best Score:", max(scores), "| Worst Score:", min(scores), "| Mean Score:", np.mean(scores),
                      "|")
                print()

            self.log_df = self.log_df.append({"generation": gen + 1, "population": members, "scores": scores},
                                             ignore_index=True)
        if csv_path is not None:
            self.log_df.to_csv(csv_path)
