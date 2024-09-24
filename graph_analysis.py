import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx
import plotly.graph_objects as go
from collections import Counter


def graph_analysis_page():
    st.title("Graph Analysis")

    if 'graph' not in st.session_state:
        st.warning("Please generate a graph first.")
        return

    G = st.session_state['graph']

    st.subheader("Graph Statistics")
    st.write(f"Number of nodes: {G.number_of_nodes()}")
    st.write(f"Number of edges: {G.number_of_edges()}")
    st.write(f"Average degree: {sum(dict(G.degree()).values()) / G.number_of_nodes():.2f}")
    st.write(f"Density: {nx.density(G):.4f}")
    st.write(f"Number of connected components: {nx.number_connected_components(G)}")

    st.subheader("Node Type Distribution")
    node_types = [data['group'] for _, data in G.nodes(data=True)]
    type_counts = Counter(node_types)
    fig, ax = plt.subplots()
    ax.bar(type_counts.keys(), type_counts.values())
    ax.set_xlabel("Node Type")
    ax.set_ylabel("Count")
    ax.set_title("Distribution of Node Types")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    st.subheader("Degree Distribution")
    degrees = [d for n, d in G.degree()]
    fig, ax = plt.subplots()
    ax.hist(degrees, bins=20)
    ax.set_xlabel("Degree")
    ax.set_ylabel("Frequency")
    ax.set_title("Degree Distribution")
    st.pyplot(fig)

    st.subheader("Network Visualization")
    if st.button("Generate Network Visualization"):
        fig = visualize_network(G)
        st.plotly_chart(fig)

    st.subheader("Centrality Analysis")
    st.write("""
        Centrality measures help identify the most important nodes in a network. Here's what each measure means:

        - **Degree Centrality**: Measures the number of connections a node has. Nodes with high degree centrality are 
          often considered influential because they have many direct connections.

        - **Betweenness Centrality**: Measures how often a node lies on the shortest path between other nodes. 
          Nodes with high betweenness centrality are important for information flow in the network.

        - **Closeness Centrality**: Measures how close a node is to all other nodes in the network. 
          Nodes with high closeness centrality can quickly interact with all other nodes.
        """)

    centrality_option = st.selectbox(
        "Choose a centrality measure",
        ["Degree Centrality", "Betweenness Centrality", "Closeness Centrality"]
    )
    if centrality_option == "Degree Centrality":
        centrality = nx.degree_centrality(G)
    elif centrality_option == "Betweenness Centrality":
        centrality = nx.betweenness_centrality(G)
    else:
        centrality = nx.closeness_centrality(G)

    top_nodes = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:10]
    st.write(f"Top 10 nodes by {centrality_option}:")
    for node, value in top_nodes:
        st.write(f"- {G.nodes[node]['label']}: {value:.4f}")

    st.subheader("Product Offering Analysis")
    st.write("""
        In this analysis, we look at the structure of a product offering and its components. Here's what the terms mean:

        - **Modules**: Major components or subsystems of the product offering.
        - **Make Parts**: Components that are manufactured in-house.
        - **Purchase Parts**: Components that are bought from suppliers.
        - **Module Complexity**: The number of connections (edges) a module has in the graph. 
          A higher number indicates that the module interacts with or depends on more other components, 
          suggesting it may be more complex to design, manufacture, or maintain.
        """)

    offerings = [node for node, data in G.nodes(data=True) if data['group'] == 'offering']
    selected_offering = st.selectbox("Select a Product Offering", offerings, format_func=lambda x: G.nodes[x]['label'])

    if st.button("Generate Report"):
        try:
            report = generate_report(G, selected_offering)
            display_report(report, G)
        except ValueError as e:
            st.error(str(e))


def visualize_network(G):
    pos = nx.spring_layout(G)
    edge_x, edge_y = [], []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines'
    )

    node_x, node_y = [], []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line_width=2
        )
    )

    node_adjacencies = []
    node_text = []
    for node, adjacencies in enumerate(G.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        node_text.append(f"Node: {G.nodes[adjacencies[0]]['label']}<br># of connections: {len(adjacencies[1])}")

    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text

    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            title='Network Graph',
            titlefont_size=16,
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20, l=5, r=5, t=40),
            annotations=[dict(
                text="",
                showarrow=False,
                xref="paper", yref="paper",
                x=0.005, y=-0.002
            )],
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
        )
    )
    return fig


def display_report(report, G):
    st.write(f"### Report for {report['offering_name']}")
    st.write(f"Number of Modules: {report['num_modules']}")
    st.write(f"Number of Make Parts: {report['num_make_parts']}")
    st.write(f"Number of Purchase Parts: {report['num_purchase_parts']}")

    fig = visualize_report(report)
    st.pyplot(fig)

    st.subheader("Module Complexity")
    module_complexity = report['module_complexity']
    for module, complexity in module_complexity.items():
        st.write(f"- {G.nodes[module]['label']}: {complexity}")

    st.subheader("Detailed Part List")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("#### Modules")
        for module in report['modules']:
            st.write(f"- {G.nodes[module]['label']}")
    with col2:
        st.write("#### Make Parts")
        for part in report['make_parts']:
            st.write(f"- {G.nodes[part]['label']}")

    with col3:
        st.write("#### Purchase Parts")
        for part in report['purchase_parts']:
            st.write(f"- {G.nodes[part]['label']}")

def generate_report(G, offering_id):
    if offering_id not in G.nodes or G.nodes[offering_id]['group'] != 'offering':
        raise ValueError(f"{offering_id} is not a valid offering node.")

    subgraph = nx.ego_graph(G, offering_id)
    modules = [node for node in subgraph.nodes() if G.nodes[node]['group'] == 'module']
    make_parts = [node for node in subgraph.nodes() if G.nodes[node]['group'] == 'make']
    purchase_parts = [node for node in subgraph.nodes() if G.nodes[node]['group'] == 'purchase']
    module_complexity = {module: len(list(G.neighbors(module))) for module in modules}

    report = {
        'offering_id': offering_id,
        'offering_name': G.nodes[offering_id]['label'],
        'num_modules': len(modules),
        'num_make_parts': len(make_parts),
        'num_purchase_parts': len(purchase_parts),
        'module_complexity': module_complexity,
        'modules': modules,
        'make_parts': make_parts,
        'purchase_parts': purchase_parts
    }

    return report


def visualize_report(report):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # Pie chart for part distribution
    parts = ['Modules', 'Make Parts', 'Purchase Parts']
    sizes = [report['num_modules'], report['num_make_parts'], report['num_purchase_parts']]
    ax1.pie(sizes, labels=parts, autopct='%1.1f%%', startangle=90)
    ax1.set_title('Distribution of Parts')

    # Bar chart for module complexity
    modules = list(report['module_complexity'].keys())
    complexity = list(report['module_complexity'].values())
    ax2.bar(modules, complexity)
    ax2.set_title('Module Complexity')
    ax2.set_xlabel('Modules')
    ax2.set_ylabel('Complexity (Number of connections)')
    ax2.tick_params(axis='x', rotation=45)

    plt.suptitle(f"Report for {report['offering_name']}")
    plt.tight_layout()
    return fig
