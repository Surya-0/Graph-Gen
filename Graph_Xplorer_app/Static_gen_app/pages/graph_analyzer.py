# graph_analyzer.py

import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
import community


def analyze_graph(G):
    analysis = {}

    analysis['num_nodes'] = G.number_of_nodes()
    analysis['num_edges'] = G.number_of_edges()

    # Count different node types
    node_types = defaultdict(int)
    for _, data in G.nodes(data=True):
        node_type = data.get('type', 'unknown')
        node_types[node_type] += 1
    analysis['node_types'] = dict(node_types)

    # Degree distribution
    in_degree_dist = [d for _, d in G.in_degree()]
    out_degree_dist = [d for _, d in G.out_degree()]
    analysis['in_degree_dist'] = in_degree_dist
    analysis['out_degree_dist'] = out_degree_dist

    # Centrality measures
    degree_centrality = nx.degree_centrality(G)
    betweenness_centrality = nx.betweenness_centrality(G)
    analysis['top_degree_centrality'] = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:5]
    analysis['top_betweenness_centrality'] = sorted(betweenness_centrality.items(), key=lambda x: x[1], reverse=True)[
                                             :5]

    # Connectivity analysis
    analysis['is_strongly_connected'] = nx.is_strongly_connected(G)
    analysis['num_strongly_connected_components'] = nx.number_strongly_connected_components(G)

    # Path analysis
    if analysis['is_strongly_connected']:
        analysis['avg_shortest_path_length'] = nx.average_shortest_path_length(G)
    else:
        largest_scc = max(nx.strongly_connected_components(G), key=len)
        scc_subgraph = G.subgraph(largest_scc)
        analysis['avg_shortest_path_length_largest_scc'] = nx.average_shortest_path_length(scc_subgraph)

    # Community detection
    partition = community.best_partition(G.to_undirected())
    modularity = community.modularity(partition, G.to_undirected())
    analysis['num_communities'] = len(set(partition.values()))
    analysis['modularity'] = modularity

    return analysis


def get_product_offering_components(G, product_offering_id):
    if product_offering_id not in G.nodes():
        return None, "Product offering not found"

    components = {
        'modules': [],
        'parts': []
    }

    def dfs_components(node, depth=0):
        if depth > 2:  # Limit depth to avoid going too far in the graph
            return
        node_data = G.nodes[node]
        if node_data['type'] == 'module':
            components['modules'].append(node_data['name'])
        elif node_data['type'] == 'part':
            components['parts'].append(node_data['name'])

        for neighbor in G.successors(node):
            dfs_components(neighbor, depth + 1)

    dfs_components(product_offering_id)

    return components, "Components retrieved successfully"


def find_shortest_path(G, start_node, end_node):
    try:
        path = nx.shortest_path(G, start_node, end_node)
        return path, "Shortest path found"
    except nx.NetworkXNoPath:
        return None, "No path exists between the specified nodes"
    except nx.NodeNotFound:
        return None, "One or both of the specified nodes do not exist in the graph"


def get_subgraph(G, node_id, depth=1):
    subgraph_nodes = {node_id}
    current_nodes = {node_id}

    for _ in range(depth):
        next_nodes = set()
        for node in current_nodes:
            next_nodes.update(G.successors(node))
            next_nodes.update(G.predecessors(node))
        subgraph_nodes.update(next_nodes)
        current_nodes = next_nodes

    return G.subgraph(subgraph_nodes)