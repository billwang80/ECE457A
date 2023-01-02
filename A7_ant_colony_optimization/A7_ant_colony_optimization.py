import pandas as pd
import matplotlib.pyplot as plt
import math
import random

df = pd.read_excel('Assignment7-city coordinates.xlsx', engine='openpyxl')
data = df.values

# set up constants
NUM_ITERATIONS = 20
ANT_MAX = 100
DECAY = 0.01
ARTIFICIAL_PHEREMONE = 0.1

# calc dist between 2 points
def distance(c1, c2):
  return math.sqrt((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2)

def ant_colony_optimization():
  path_sums = []

  for _ in range(NUM_ITERATIONS):
    # initialize artificial pheremone
    pheremone = {}
    for i in range(1,29): # where 1 to 29 is id of cities
      for j in range(i+1,30):
        pheremone[(i,j)] = ARTIFICIAL_PHEREMONE

    # for each ant
    path_sums_iteration = []
    for cur_ant in range(ANT_MAX):
      visited = set()
      cur_city = 1
      path_sum = 0

      # while not all cities are visited
      while len(visited) < 28:
        # see if city has been visited
        visited.add(cur_city)

        # generate probability list 
        pheremone_sum = 0
        probability_list = []
    
        for i in range(1,30):
          if i != cur_city and i not in visited:
            path = (min(cur_city, i), max(cur_city, i))
            pheremone_sum += pheremone[path]
            probability_list.append([path, pheremone[path]])

        # selecting path
        rand = random.uniform(0, pheremone_sum)
        cur_rand = probability_list[0][1]
        i = 0
        while cur_rand < rand:
          i += 1
          cur_rand += probability_list[i][1]
        
        selected_path = probability_list[i][0]
        if cur_city == selected_path[0]:
          cur_city = selected_path[1]
        else:
          cur_city = selected_path[0]

        # evaporate phermones
        for i in range(1,29):
          for j in range(i+1,30):
            pheremone[(i,j)] = pheremone[(i,j)] * (1 - DECAY)
        
        # add pheremone
        city1 = data[selected_path[0] - 1]
        city2 = data[selected_path[1] - 1]
        coordinate1 = [city1[1], city1[2]]
        coordinate2 = [city2[1], city2[2]]
        pheremone[selected_path] = pheremone[selected_path] + 1/distance(coordinate1, coordinate2)

        path_sum += distance(coordinate1, coordinate2)
      path_sums_iteration.append(path_sum)
    path_sums.append(path_sums_iteration)
  return path_sums

res = ant_colony_optimization()

m = len(res)
n = len(res[0])

average_res = []
best_res = []

# find avg fitness and best fitness
for j in range(n):
  avg_fitness = 0
  best_fitness = 0
  for i in range(m):
    best_fitness = max(best_fitness, 1/res[i][j])
    avg_fitness += 1/res[i][j]
  avg_fitness /= m
  average_res.append(avg_fitness)
  best_res.append(best_fitness)

plt.figure()
plt.plot(average_res, color='r', label='average fitness')
plt.plot(best_res, color='b', label='best fitness')
plt.xlabel('Iteration number')
plt.ylabel('Fitness')
plt.title('Best and Average Fitness vs Iteration')
plt.show()

# print(res)