import random
import matplotlib.pyplot as plt

# fitness can be -1 * camelback
def camelback(x,y):
  # divide by 1000 to convert to actual number between -5 and 5
  x /= 1000
  y /= 1000
  return (4-2.1*x**2 + x**4/3)*x**2 + x*y + (-4+4*y**2)*y**2

def fitness(x,y):
  # remove probability of parent selection if outside of range
  if x > 5000 or x < -5000 or y > 5000 or y < -5000:
    return 0
  # offset by a large number to remove negative values, then inverse
  return 1/(camelback(x,y) + 50)

# convert 2s complement string to int
# num is a string
def decode(num, bits=16):
  num = int(num,2)
  if (num & (1 << (bits - 1))) != 0:
    num = num - (1 << bits)
  return num

# convert int to 2s complement string
def encode(num, bits=16):
  if num < 0:
    num = num + (1 << bits)
  format_string = "{:0%ib}" % bits
  return format_string.format(num)

# create initial generation
def generate_gen_one(pop_size):
  generation = []
  avg_fitness = 0
  for i in range(pop_size):
    generation.append([round(random.uniform(-5000, 5000)), round(random.uniform(-5000, 5000))])
    generation[i].append(fitness(generation[i][0], generation[i][1]))
    avg_fitness += generation[i][2]
  return [generation, avg_fitness/len(generation)]

def create_children_1_point(parent1, parent2):
  parent1 = [encode(parent1[0]), encode(parent1[1])]
  parent2 = [encode(parent2[0]), encode(parent2[1])]

  cross_point1 = round(random.uniform(0, len(parent1[0])))
  cross_point2 = round(random.uniform(0, len(parent1[1])))

  temp = parent1
  parent1 = [
    decode(parent1[0][:cross_point1] + parent2[0][cross_point1:]), 
    decode(parent1[1][:cross_point2] + parent2[1][cross_point2:])
  ]
  parent2 = [
    decode(parent2[0][:cross_point1] + temp[0][cross_point1:]), 
    decode(parent2[1][:cross_point2] + temp[1][cross_point2:])
  ]

  parent1.append(fitness(parent1[0], parent1[1]))
  parent2.append(fitness(parent2[0], parent2[1]))

  return [parent1, parent2]


POP_SIZE = 1000
GENERATIONS = 100

# return [x,y,z]
def simple_genetic_algorithm():
  avg_fitness_arr = []
  best_fitness_arr = []
  res = [0,0,0]

  # create initial generation
  generation_one = generate_gen_one(POP_SIZE)
  generation = generation_one[0] # [x,y,fitness] 
  # print(generation)
  avg_fitness_arr.append(generation_one[1])
  
  for _ in range(GENERATIONS):
    next_gen = []
    avg_fitness = 0
    # parent selection
    for pop in range(POP_SIZE // 2):
      # spin wheel
      fitness_selection = random.uniform(0, avg_fitness_arr[-1]*len(generation))
      i = -1
      while fitness_selection > 0:
        i += 1
        fitness_selection -= generation[i][2]
      parent1 = generation[i]
      # spin wheel again
      fitness_selection = random.uniform(0, avg_fitness_arr[-1]*len(generation))
      i = -1
      while fitness_selection > 0:
        i += 1
        fitness_selection -= generation[i][2]
      parent2 = generation[i]
      # create children
      children = create_children_1_point(parent1, parent2)
      next_gen.append(children[0])
      next_gen.append(children[1])
      avg_fitness += children[0][2] + children[1][2]
    
    generation = next_gen
    avg_fitness /= len(generation)
    avg_fitness_arr.append(avg_fitness)
    generation = sorted(generation, key=lambda x: x[2])
    best_fitness_arr.append(generation[-1][2])

    if res[2] < best_fitness_arr[-1]:
      res = generation[-1]
      
  print("x: ", generation[-1][0]/1000)
  print("y: ", generation[-1][1]/1000)
  print("z: ", camelback(generation[-1][0], generation[-1][1]))

  plt.figure()
  plt.plot(avg_fitness_arr)
  plt.xlabel('Generation number')
  plt.ylabel('Avg Fitness')
  plt.title('Avg Fitness vs Generation')
  plt.show()

  plt.figure()
  plt.plot(best_fitness_arr)
  plt.xlabel('Generation number')
  plt.ylabel('Best Fitness')
  plt.title('Best Fitness vs Generation')
  plt.show()

simple_genetic_algorithm()
