import csv

distance_file = open('A5-Distance.csv', 'r')
flow_file = open('A5-Flow.csv', 'r')

distance_data = list(csv.reader(distance_file, quoting=csv.QUOTE_NONNUMERIC))
flow_data = list(csv.reader(flow_file, quoting=csv.QUOTE_NONNUMERIC))

# return cost
# i + 5 < m and j + 5 < n
def total_cost(x,y):
  cost = 0
  for i in range(x, x+6):
    for j in range(y, y+6):
      cost += (distance_data[i][j] * flow_data[i][j])
  # print(cost)
  return cost


# return cost and list of coordinates of each building
def tabu_search():
  m = len(distance_data)
  n = len(distance_data[0])

  N = m*n

  res = float('inf')
  for i in range(m-5):
    for j in range(n-5):
      res = min(res, total_cost(i,j))

  return res

print(tabu_search())