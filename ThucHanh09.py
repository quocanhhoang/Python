import networkx as nx
import matplotlib.pyplot as plt

node = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'}
edge = {('A', 'E'), ('A', 'C'), ('A', 'B'), ('B', 'D'), ('B', 'F'), ('C', 'G'), ('C', 'F'), ('C', 'D'), ('D', 'E'), ('D', 'H'), ('E', 'G'), ('E', 'F'), ('F', 'H'), ('H', 'G')}

đồ_thị = nx.DiGraph(edge)
pos = {
    'G':(1.0, 0.0),
    'H':(4.0, 0.0),
    'E':(2.0, 1.5),
    'F':(3.0, 1.5),
    'C':(2.0, 3.0),
    'D':(3.0, 3.0),
    'A':(1.0, 4.5),
    'B':(4.0, 4.5),
}

nx = nx.draw(đồ_thị, pos, with_labels=True)
plt.show()