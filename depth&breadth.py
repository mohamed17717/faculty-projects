  ## Adjacency graph matrix must be square
  ## cus its relation between nodes on clm and others in rows
  ## write a function to change Adjacency matrix to dict
graph1 = [
 # 1,2,3,4
  [0,1,1,1], #1
  [1,0,1,0], #2
  [1,1,0,0], #3
  [1,0,0,0]  #4
]

graph = {
  '1': ('2','3','4'),
  '2': ('1', '3'),
  '3': ('1', '2'),
  '4': ('1')
}

graph = {
  'a': ('b', 'd', 'g'),
  'b': ('a', 'e', 'f'),
  'c': ('f', 'h'),
  'd': ('a', 'f'),
  'e': ('b', 'g'),
  'f': ('b', 'c', 'd'),
  'g': ('a', 'e'),
  'h': ('c'),
}



def graph_adjencyToDict(graph):
  ## nodes have no names so i use increment value 0,1,2,.....
  ## make dict_graph ready with nodes names
  nodes_count = len(graph)
  dict_graph  = {}
  [dict_graph.update({i: []}) for i in range(nodes_count)]

  ## go throw nodes names and row indexes
  for i in range(nodes_count):
    row = graph[i]

    ## node.append(relational_node)
    ## enumerate to get node name(index) to the value and chck the value if not 0
    [dict_graph[i].append(index) for index, relation in enumerate(row) if relation]

  return dict_graph

#print(graph_adjencyToDict(graph1))

## Graph Algorithms
# Depth First Search and Bredth

# depath and bredth difference is the first depend on stack other depend on queue
# stack rule (last in first out)
# queue rule (first in first out)

def get_next_node(relations, visited):
  for relation in relations: 
    if relation not in visited:
      return relation
  return None

def depth(graph):
  stack   = []
  visited = []

  ## start (doesn't matter which)
  strat_node = tuple(graph.keys())[0]
  
  stack.append(strat_node)
  visited.append(strat_node)
  
  while stack:
    current_node = stack[-1]
    relations    = graph[current_node]

    next_node = get_next_node(relations, visited)
    if next_node:
      stack.append(next_node)
      visited.append(next_node)
    else:
      stack.pop()

  return visited

def breadth(graph):
  queue   = []
  visited = []

  ## start (doesn't matter which)
  strat_node = tuple(graph.keys())[0]
  
  queue.append(strat_node)
  visited.append(strat_node)

  while queue: 
    current_node = queue[0]
    relations    = graph[current_node]

    next_node = get_next_node(relations, visited)
    if next_node:
      queue.append(next_node)
      visited.append(next_node)
    else:
      queue = queue[1:]

  return visited





# print(depth(graph))
# print(breadth(graph))

# x = [node if graph[node] for node in graph]

graph = {
  'a': ('b', 'c'),
  'b': ('a', 'g'),
  'c': ('a', 'd', 'f'),
  'd': ('c'),
  'f': ('c'),
  'g': ('b', 'o', 'h'),
  'o': ('g'),
  'h': ('g'),
}

print(depth(graph))
print(breadth(graph))