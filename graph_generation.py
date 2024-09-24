import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from constants import *
import random


def poisson_module_generation(mu=3):
    return max(1, np.random.poisson(mu))


def gaussian_part_generation(mean=5, stddev=2):
    return max(1, int(np.random.normal(mean, stddev)))


def generate_graph(total_nodes: int, density_factors: dict, module_to_part_ratio: float = 0.3):
    G = nx.Graph()

    # Add Business Group Node
    G.add_node('BG001', label='Etch', group='business_group')

    # Add Product Families and Offerings
    for family in PRODUCT_FAMILIES:
        G.add_node(family['Family_ID'], label=family['Family_Name'], group='family')
        G.add_edge('BG001', family['Family_ID'])

    for offering in PRODUCT_OFFERINGS:
        G.add_node(offering['Offering_ID'], label=offering['Offering_Name'], group='offering')
        G.add_edge(offering['Family_ID'], offering['Offering_ID'])

    # Calculate remaining nodes
    remaining_nodes = total_nodes - G.number_of_nodes()
    modules_count = int(remaining_nodes * module_to_part_ratio)
    parts_count = remaining_nodes - modules_count

    # Generate Modules and Parts using weighted random generation
    module_counter = 0
    part_counter = 0

    while G.number_of_nodes() < total_nodes:
        offering = random.choice(PRODUCT_OFFERINGS)
        offering_id = offering['Offering_ID']
        density_factor = density_factors.get(offering_id, 0.5)

        if random.random() < density_factor:
            if module_counter < modules_count:
                # Use Poisson distribution for module generation
                num_modules = poisson_module_generation(mu=int(3 * density_factor))
                for i in range(num_modules):
                    module_id = f'M_{offering_id}_{module_counter:04d}'
                    G.add_node(module_id, label=f'Module {module_counter}', group='module')
                    G.add_edge(offering_id, module_id)
                    module_counter += 1
            else:
                # Use Gaussian distribution for part generation
                num_parts = gaussian_part_generation(mean=5, stddev=2)
                for i in range(num_parts):
                    part_id = f'P_{offering_id}_{part_counter:04d}'
                    part_type = random.choice(['make', 'purchase'])
                    G.add_node(part_id, label=f'{part_type.capitalize()} Part {part_counter}', group=part_type)

                    if module_counter > 0 and random.random() < 0.7:
                        random_module = random.choice([n for n in G.nodes if G.nodes[n]['group'] == 'module'])
                        G.add_edge(random_module, part_id)
                    else:
                        G.add_edge(offering_id, part_id)
                    part_counter += 1

    print(f"Total Nodes Generated: {G.number_of_nodes()}")
    print(f"Modules: {module_counter}, Parts: {part_counter}")
    return G


def plot_entire_graph(G):
    pos = nx.spring_layout(G, k=0.5, iterations=50)
    fig, ax = plt.subplots(figsize=(20, 20))

    for group in COLOR_MAP:
        nx.draw_networkx_nodes(G, pos,
                               nodelist=[node for node, data in G.nodes(data=True) if data['group'] == group],
                               node_color=COLOR_MAP[group],
                               node_size=100,
                               alpha=0.8,
                               label=group,
                               ax=ax)

    nx.draw_networkx_edges(G, pos, alpha=0.2, ax=ax)

    ax.set_title("Full Graph Visualization")
    ax.legend()
    ax.axis('off')
    plt.tight_layout()
    return fig


def graph_generation_page():
    st.title("Graph Generation and Visualization")

    total_nodes = st.number_input("Enter the total number of nodes:", min_value=100, max_value=10000, value=1000,
                                  step=100)

    if st.button("Generate Graph"):
        density_factors = {
            'PO001': 0.7, 'PO002': 0.6, 'PO003': 0.8, 'PO004': 0.5, 'PO005': 0.6,
            'PO006': 0.7, 'PO007': 0.5, 'PO008': 0.9, 'PO009': 0.4, 'PO010': 0.7,
            'PO011': 0.6, 'PO012': 0.5, 'PO013': 0.8, 'PO014': 0.7, 'PO015': 0.6,
            'PO016': 0.9, 'PO017': 0.7, 'PO018': 0.8, 'PO019': 0.5, 'PO020': 0.6,
            'PO021': 0.4
        }

        G = generate_graph(total_nodes=total_nodes, density_factors=density_factors, module_to_part_ratio=0.3)
        st.session_state['graph'] = G
        st.success(f"Graph generated with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")

        fig = plot_entire_graph(G)
        st.pyplot(fig)
