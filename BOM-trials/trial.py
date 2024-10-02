import pickle
import networkx
import networkx as nx


def load_graph(filename='supply_chain_graph.pkl'):
    with open(filename, 'rb') as f:
        return pickle.load(f)

G = load_graph()
print(len(G.nodes))

print(G.nodes['PO_001'])