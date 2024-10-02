import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
import pickle


def load_graph(filename='supply_chain_graph.pkl'):
    with open(filename, 'rb') as f:
        return pickle.load(f)


def analyze_graph(G):
    print("Graph Analysis:")
    print(f"Number of nodes: {G.number_of_nodes()}")
    print(f"Number of edges: {G.number_of_edges()}")

    # Count different node types
    node_types = {
        'business_group': 0,
        'product_families': 0,
        'product_offerings': 0,
        'modules': 0,
        'parts': 0
    }
    for node, data in G.nodes(data=True):
        node_types[data['type']] += 1

    for node_type, count in node_types.items():
        print(f"Number of {node_type}: {count}")

    # Degree distribution
    in_degree_dist = [d for n, d in G.in_degree()]
    out_degree_dist = [d for n, d in G.out_degree()]

    plt.figure(figsize=(12, 6))
    plt.subplot(121)
    plt.hist(in_degree_dist, bins=20)
    plt.title("In-degree Distribution")
    plt.xlabel("In-degree")
    plt.ylabel("Frequency")

    plt.subplot(122)
    plt.hist(out_degree_dist, bins=20)
    plt.title("Out-degree Distribution")
    plt.xlabel("Out-degree")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig("degree_distribution.png")
    plt.close()

    # Centrality measures
    print("\nTop 5 nodes by degree centrality:")
    degree_centrality = nx.degree_centrality(G)
    for node, centrality in sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"{node}: {centrality:.4f}")

    print("\nTop 5 nodes by betweenness centrality:")
    betweenness_centrality = nx.betweenness_centrality(G)
    for node, centrality in sorted(betweenness_centrality.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"{node}: {centrality:.4f}")

    # Connectivity analysis
    print(f"\nIs the graph strongly connected? {nx.is_strongly_connected(G)}")
    print(f"Number of strongly connected components: {nx.number_strongly_connected_components(G)}")

    # Path analysis
    if nx.is_strongly_connected(G):
        print("\nAverage shortest path length:", nx.average_shortest_path_length(G))
    else:
        print("\nGraph is not strongly connected. Cannot calculate average shortest path length.")
        # Optionally, calculate the average shortest path length for the largest strongly connected component:
        largest_scc = max(nx.strongly_connected_components(G), key=len)
        scc_subgraph = G.subgraph(largest_scc)
        print(
            f"Average shortest path length in the largest strongly connected component: {nx.average_shortest_path_length(scc_subgraph):.4f}")

    # Community detection (using Louvain method)
    try:
        import community
        partition = community.best_partition(G.to_undirected())
        modularity = community.modularity(partition, G.to_undirected())
        print(f"\nNumber of communities detected: {len(set(partition.values()))}")
        print(f"Modularity: {modularity:.4f}")
    except ImportError:
        print("\nCommunity detection requires the 'python-louvain' package. Please install it to use this feature.")


def main():
    G = load_graph()
    analyze_graph(G)


if __name__ == "__main__":
    main()