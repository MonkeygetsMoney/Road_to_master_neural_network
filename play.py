# experiment with the class object and methods in util.py

from util import Node, StackFrontier, QueueFrontier

# root
a = Node(state='A', parent=None, action=None)
# ranch out to B and C
b = Node(state='B', parent=a, action='first move')
d = Node(state='D', parent=b, action='second move')
e = Node(state='E', parent=b, action='second move')

c = Node(state='C', parent=a, action='first move')
f = Node(state='F', parent=c, action='second move')

# node = c
# while node.parent is not None:
#     print('Came from', node.parent.state, 'via', node.action)
#     node = node.parent # walking backward, set as the previous node

# implement two frontiers
stack = StackFrontier() # last-in first-out
queue = QueueFrontier() # first-in first-out

# a would be the starting point so add to the frontier
stack.add(a)
queue.add(a)
goal_state = 'F' # defined the goal state

while True:
    node = stack.remove()
    if node.state == goal_state:
        actions = []

        # walking backward like in the lecture
        while node.parent is not None:
            actions.append(node.action)

        print(actions.reverse())
        break

    else:
        for n in [b, c, d, e, f]:
            if n.parent == node:
                stack.add(n)

for n in [a, b, c]:
    stack.add(n) # add the node to the frontier
    queue.add(n)

print('Stack order:')
while not stack.empty():
    print(stack.remove().state)

print('Queue order:')
while not queue.empty():
    print(queue.remove().state)