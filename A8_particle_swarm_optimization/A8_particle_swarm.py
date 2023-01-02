import random
import matplotlib.pyplot as plt

# fitness can be -1 * camelback
def camelback(x,y):
  # divide by 1000 to convert to actual number between -5 and 5
  return (4-2.1*x**2 + x**4/3)*x**2 + x*y + (-4+4*y**2)*y**2

def fitness(x,y):
  # remove probability of parent selection if outside of range
  if x > 5 or x < -5 or y > 5 or y < -5:
    return 0
  # offset by a large number to remove negative values, then inverse
  return 1/(camelback(x,y) + 50)

# initialize swarm pos and velocity
def initialize_swarm(pop_size, v_max, v_min):
  swarm_position = []
  swarm_velocity = []
  swarm_performance = []

  for i in range(pop_size):
    swarm_position.append([random.uniform(-5, 5), random.uniform(-5, 5)])

    # randomly choose pos or neg direction
    x_direction = 1 if random.uniform(-1,1) >= 0 else -1
    y_direction = 1 if random.uniform(-1,1) >= 0 else -1

    swarm_velocity.append([random.uniform(v_min, v_max) * x_direction, random.uniform(v_min, v_max) * y_direction])
    swarm_performance.append(fitness(swarm_position[i][0], swarm_position[i][1]))

  return [swarm_position, swarm_velocity, swarm_performance]

# parameters
POP_SIZE = 100
ITERATIONS = 500
V_MAX = 0.5
V_MIN = 0
W = 0.8
C1 = 0.3
C2 = 0.3

def particle_swarm():
  # initialize swarm
  swarm_position, swarm_velocity, swarm_performance = initialize_swarm(POP_SIZE, V_MAX, V_MIN)

  avg_fitness_arr = []
  best_fitness_arr = []
  res = []
  res_value = 0

  t = 1
  while t < ITERATIONS:
    best_index = -1
    best_performance = 0
    avg_performance = 0

    for i in range(POP_SIZE): # for each particle
      # find best and avg performance
      cur_fitness = fitness(swarm_position[i][0], swarm_position[i][1])
      if cur_fitness > best_performance:
        best_index = i
        best_performance = cur_fitness
      avg_performance += cur_fitness

      # update res
      if best_performance > res_value:
        res_value = best_performance
        res = swarm_position[best_index]
      # find this particle best performance
      swarm_performance[i] = max(swarm_performance[i], cur_fitness)

      g = best_index
      # find best neighbour
      for j in range(i+1, POP_SIZE):
        if fitness(swarm_position[j][0], swarm_position[j][1]) > fitness(swarm_position[g][0], swarm_position[g][1]):
          g = j

      # new speed 
      swarm_velocity[i][0] = swarm_velocity[i][0]*W + C1*random.uniform(0,1)*(swarm_performance[i] - cur_fitness) + C2*random.uniform(0,1)*(fitness(swarm_position[g][0], swarm_position[g][1]) - cur_fitness)
      swarm_velocity[i][1] = swarm_velocity[i][1]*W + C1*random.uniform(0,1)*(swarm_performance[i] - cur_fitness) + C2*random.uniform(0,1)*(fitness(swarm_position[g][0], swarm_position[g][1]) - cur_fitness)

      # ensure velocity is within vmax and vmin
      if swarm_velocity[i][0] > V_MAX:
        swarm_velocity[i][0] = V_MAX
      elif swarm_velocity[i][0] < V_MIN:
        swarm_velocity[i][0] = V_MIN
      if swarm_velocity[i][1] > V_MAX:
        swarm_velocity[i][1] = V_MAX
      elif swarm_velocity[i][1] < V_MIN:
        swarm_velocity[i][1] = V_MIN

      # new position
      swarm_position[i][0] = max(-5, min(5, swarm_position[i][0] + swarm_velocity[i][0]))
      swarm_position[i][1] = max(-5, min(5, swarm_position[i][1] + swarm_velocity[i][1]))

    # update best and avg performance
    avg_fitness_arr.append(avg_performance/POP_SIZE)
    best_fitness_arr.append(best_performance)

    t += 1

  return [res, res_value, avg_fitness_arr, best_fitness_arr]

res = particle_swarm()

# print(res[2])
# print(res[3])
print("Best:", res[0])
print("Best fitness:", res[1])
print("Best value:", camelback(res[0][0], res[0][1]))

plt.figure()
plt.plot(res[2])
plt.xlabel('Iteration number')
plt.ylabel('Avg Fitness')
plt.title('Avg Fitness vs Iteration')
plt.show()

plt.figure()
plt.plot(res[3])
plt.xlabel('Iteration number')
plt.ylabel('Best Fitness')
plt.title('Best Fitness vs Iteration')
plt.show()
