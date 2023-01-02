import random
import math

def easom(x, y):
  return -1*math.cos(x)*math.cos(y)*math.exp(-1*(x-math.pi)**2 - (y-math.pi)**2)

# print(easom(-11.171838173101502, 0.17868216957983307))

def simulated_annealing(start, anneal_schedule, step_size, temperature, alpha, stop_temp):
  best_point = start
  best_cost = easom(best_point[0], best_point[1])

  cur_point = best_point
  cur_cost = best_cost

  while temperature > stop_temp:
    new_point = [
      random.uniform(max(-100, cur_point[0] - step_size), min(100, cur_point[0] + step_size)),
      random.uniform(max(-100, cur_point[1] - step_size), min(100, cur_point[1] + step_size))
    ]

    new_cost = easom(new_point[0], new_point[1])

    if new_cost < best_cost:
      best_point = new_point
      best_cost = new_cost

    cost_diff = new_cost - cur_cost

    if cost_diff < 0:
      cur_point = new_point
      cur_cost = new_cost
    else:
      x = random.uniform(0,1)
      if x < math.exp(-cost_diff/temperature):
        cur_point = new_point
        cur_cost = new_cost

    if anneal_schedule == 'linear':
      temperature -= alpha
    elif anneal_schedule == 'geometric':
      temperature *= alpha

  return [best_point, best_cost]

# part b
anneal_schedule = "linear"
step_size = 20
temperature = 0.01
alpha = 0.00001
stop_temp = 0

start = [random.uniform(-100,100), random.uniform(-100,100)]
res = simulated_annealing(start, anneal_schedule, step_size, temperature, alpha, stop_temp)
print("Final Point: ", res[0])
print("Final Cost: ", res[1])

# part c
optimal_start = []
optimal_point = []
optimal_value = float('inf')
test_list = []

for i in range(10):
  start = [random.uniform(-100,100), random.uniform(-100,100)]
  test = simulated_annealing(start, anneal_schedule, step_size, temperature, alpha, stop_temp)
  test_list.append(start)
  if test[1] < optimal_value:
    optimal_start = start
    optimal_point = test[0]
    optimal_value = test[1]

print(test_list)
print("Optimal start:", optimal_start)
print("Optimal point:", optimal_point)
print("Optimal value:", optimal_value)

# part d
temp_list = [0.0025, 0.005, 0.025, 0.05]

for temp in temp_list:
  res = simulated_annealing(start, anneal_schedule, step_size, temp, alpha, stop_temp)
  print("Temp = ", temp)
  print("Result:", res)

# part e
anneal_schedule = "geometric"
step_size = 20
temperature = 0.01
alpha = 0.999
stop_temp = 0.00001
res = simulated_annealing(start, anneal_schedule, step_size, temp, alpha, stop_temp)
print("Final Point: ", res[0])
print("Final Cost: ", res[1])
