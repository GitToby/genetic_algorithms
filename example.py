import random
import numpy as np
import src as ga


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
    if height_diff > 0 or width_diff > 0:
        return 1 / (height_diff + width_diff)
    else:
        return np.inf


def param_generator():
    max_h = 10
    max_w = 20
    yield {'height': random.randrange(max_h),
           'width': random.randrange(max_w)}


random.seed(1)
pop = ga.Population(10, Door, fit_through_door, member_parameters_generator=param_generator)

# run 5 generations before checking we have some parameters changed
pop.run(generations=500, print_logging=True)
print(pop.get_top())
