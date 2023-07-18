#! /usr/bin/python3

"""Make genetic algorithm breeding 4 males and 16 females"""

import time
import random
import statistics
from itertools import cycle

GOAL = 50000

NUM_RATS = 20
NUM_MALE = 1
NUM_FEMALE = NUM_RATS - NUM_MALE

MIN_FEMALE_WT  = 200
MAX_FEMALE_WT  = 300
MODE_FEMALE_WT = 250

MIN_MALE_WT  = 301
MAX_MALE_WT  = 600
MODE_MALE_WT = 350

MALE_BORN_PROB = 0.51

MUTATE_ODDS = 0.01
MUTATE_MIN  = 0.50
MUTATE_MAX  = 1.20

LITTER_SIZE = 8
LITTERS_PER_YEAR = 10
GENERATION_LIMIT = 500

def populate(num_rats, min_wt, max_wt, mode_wt):
  return [int(random.triangular(min_wt, max_wt, mode_wt)) for i in range(num_rats)]

def fitness(population, goal):
  ave = statistics.mean(population)
  return ave / goal

def select(mals, fems, to_retain_male, to_retain_female):
  sorted_males   = sorted(mals)
  sorted_females = sorted(fems)
  
  selected_males   = sorted_males[-to_retain_male:]
  selected_females = sorted_females[-to_retain_female:]
  return selected_males, selected_females

def breed(males, females, litter_size):
  random.shuffle(males)
  random.shuffle(females)
  children = []
  zipped_list = list(zip(cycle(males), females))
  
  for male, female in zipped_list:
    for child in range(litter_size):
      child = random.randint(female, male)
      children.append(child)
  return children

def mutate(children, mutate_odds, mutate_min, mutate_max):
  for index, rat in enumerate(children):
    if mutate_odds >= random.random():
      children[index] = round(rat * random.uniform(mutate_min, mutate_max))
  return children

def split_children(children, male_prob):
  sorted_children = sorted(children)
  female_members  = len(children) - round(len(children) * male_prob)
  female_children = sorted_children[:female_members]
  male_children   = sorted_children[female_members:]
  return male_children, female_children


def main():
  generations  = 0
  
  male_parents   = populate(NUM_MALE, MIN_MALE_WT, MAX_MALE_WT, MODE_MALE_WT)
  female_parents = populate(NUM_FEMALE, MIN_FEMALE_WT, MAX_FEMALE_WT, MODE_FEMALE_WT)
  
  parents = male_parents + female_parents
  
  print("initial population weights = {}".format(parents))
  popl_fitness = fitness(parents, GOAL)
  print("initial population fitness = {}".format(popl_fitness))
  print("number to retain = {}".format(NUM_RATS))

  ave_wt = []
  
  while popl_fitness < 1 and generations < GENERATION_LIMIT:
    selected_males, selected_females = select(male_parents, female_parents,  NUM_MALE, NUM_FEMALE)
    children = breed(selected_males, selected_females, LITTER_SIZE)
    children = mutate(children, MUTATE_ODDS, MUTATE_MIN, MUTATE_MAX)
    male_children, female_children = split_children(children, MALE_BORN_PROB)
    male_parents   = selected_males + male_children
    female_parents = selected_females + female_children
    parents = male_parents + female_parents
    popl_fitness = fitness(parents, GOAL)
    
    print("Generation {} fitness {:.4f}".format(generations, popl_fitness))
    ave_wt.append(int(statistics.mean(parents)))
    generations += 1
    
  print("Average weight per generation = {}".format(ave_wt))
  print("\nnumber of generations = {}".format(generations))
  print("number of years = {}".format(int(generations / LITTERS_PER_YEAR)))


if __name__ == '__main__':
    start_time = time.time()
    main()
    end_time = time.time()
    duration = end_time - start_time
    print("\nRuntime for this program was {} seconds.".format(duration))
