# Genetic Algorithms for python
[![Build Status](https://travis-ci.org/GitToby/genetic_algorithms.svg?branch=master)](https://travis-ci.org/GitToby/genetic_algorithms)

This library is a wrapper for genetic algorithms to leverage in optimisation problems.
It hopes to make writing infinitely customizable genetic algorithms easy and quick while having all the standard features expected.

# Installation
This module can be installed via pip:
```bash
pip install genetic-algorithms
```

# Roadmap
* add mutation potency & frequency, extract population flow to user defined sequence.
* add multi population models
* add common crossover and mutation generic methods

# Examples
This is a basic example for maximising values in a list, starting with 10 members running 100 generation.
Then it will log to the screen and create a csv file with each generations information in short format.

```python
import genetic_algorithms as ga
import random

class MyMember(ga.MemberBase):
    def _construct_from_params(self, construction_parameters=None):
        # Starting point is a bunch of 5 numbers [0-9]
        self.vars = [random.randrange(10) for _ in range(5)]

    def mutate(self):
        # Mutation involves adding a number between -2 and 2 to a random variable
        i = random.randrange(-2,3)
        j = random.randrange(len(self.vars))
        self.vars[j] += i

    def crossover(self, pairing):
        # Crossing over takes the first half from member one, and the second half from member 2
        new_params = self.vars[:len(self.vars) // 2] + pairing.vars[len(pairing.vars) // 2:]
        return MyMember(new_params)

    def score_self(self):
        return sum(self.vars)

def m_fit_func(member: MyMember):
    # This scores the member on its properties, but can involve any external functions as needed.
    # Remember to test this does what you want.
    return member.score_self()

pop = ga.Population(size=10, member_type=MyMember, member_parameters_generator=None,
                   fitness_function=m_fit_func, population_seed=0)
pop.run(100, print_logging=True, csv_path="example1.csv")
```

This next one is a little more complected; we want to identify a door of a particular size.
```python
import genetic_algorithms as ga
import random
import numpy as np


class Door(ga.MemberBase):
    def _construct_from_params(self, construction_parameters=None):
        # Set the parameters as passed by the generator
        self.height = construction_parameters['height']
        self.width = construction_parameters['width']

    def mutate(self):
        # Mutate by adding 1 or -1 to our door height and width.
        # this is an example of a bad mutation function because it wouldn't hit an integer after the mutation
        i = random.randrange(2)
        j = random.randrange(2)
        self.height += pow(-1, i)
        self.width += pow(-1, j)

    def crossover(self, pairing):
        # Again a bad example of a crossover, the mean we will converge quickly but very hard to get a precice score.
        new_params = {'height': np.mean([self.height, pairing.height]),
                      'width': np.mean([self.width, pairing.width])}
        return Door(construction_parameters=new_params)

    def __repr__(self):
        return 'height: ' + str(self.height) + " | width: " + str(self.width)


def fit_through_door(member: Door):
    door_height = 10
    door_width = 3
    height_diff = abs(door_height - member.height)
    width_diff = abs(door_width - member.width)
    return height_diff + width_diff

def param_generator():
    max_h = 10
    max_w = 20
    yield {'height': random.randrange(max_h),
           'width': random.randrange(max_w)}

random.seed(1)
pop = ga.Population(100, Door, fit_through_door, member_parameters_generator=param_generator)
# run 500 generations before checking we have some parameters changed
pop.run(generations=500, print_logging=True, maximise_fitness_func=False)
print("Best door:", pop.get_top())
# returns what almost exactly what we want:
# Best door: (height: 9.999995902180672 | width: 3.999865485355258, 244033.23286180547)
```

Finally, we will boost it to a very complicated example, we want to generate a copy of a picture of a face from a randomly generated face.
