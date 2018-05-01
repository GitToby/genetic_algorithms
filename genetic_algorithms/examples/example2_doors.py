import random
import genetic_algorithms as ga
import numpy as np


# Example 2 - Finding a door that's the right size
class Door(ga.MemberBase):
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
                      'width': np.mean([self.width, pairing.width])}
        return Door(construction_parameters=new_params)

    def __repr__(self):
        return 'height: ' + str(self.height) + " | width: " + str(self.width)


def fit_through_door(door: Door):
    door_height = 10
    door_width = 3
    height_diff = abs(door_height - door.height)
    width_diff = abs(door_width - door.width)

    if height_diff > 0 and width_diff > 0:
        return (1 / height_diff) + (1 / width_diff)
    elif height_diff == 0:
        return 1 / width_diff
    elif width_diff == 0:
        return 1 / height_diff
    else:
        return np.inf


def param_generator():
    max_h = 10
    max_w = 20
    yield {'height': random.randrange(max_h),
           'width': random.randrange(max_w)}


random.seed(1)
pop = ga.Population(100, Door, fit_through_door, member_parameters_generator=param_generator)

# run 500 generations before checking we have some parameters changed
pop.run(generations=500, print_logging=True,)
print("Best door:", pop.get_top_member())
# This will spit out a very close approximation of the true door size we selected
