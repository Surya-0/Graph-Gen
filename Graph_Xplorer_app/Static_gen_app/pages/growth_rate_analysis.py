import streamlit as st
import plotly.graph_objects as go
from .data_generator import DataGenerator
from .performance_utils import measure_performance

def analyze_growth_rate(max_nodes, step):
    nodes = list(range(26, max_nodes + 1, step))
    times = []

    for n in nodes:
        @measure_performance
        def generate_graph(total_nodes):
            generator = DataGenerator(total_nodes)
            generator.generate_data()
            return generator.get_data(), generator.get_graph()

        result = generate_graph(n)
        times.append(result[2]['execution_time'])

    return nodes, times

def plot_growth_rate(nodes, times):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=nodes, y=times, mode='lines+markers'))
    fig.update_layout(
        title='Graph Generation Time vs Number of Nodes',
        xaxis_title='Number of Nodes',
        yaxis_title='Generation Time (seconds)'
    )
    return fig

def show_growth_rate_analysis():
    st.subheader("Growth Rate Analysis")

    max_nodes = st.slider("Maximum number of nodes", min_value=100, max_value=1000000, value=2000, step=100)
    step = st.slider("Step size", min_value=10, max_value=500, value=50, step=10)

    if st.button("Analyze Growth Rate"):
        with st.spinner("Analyzing growth rate..."):
            nodes, times = analyze_growth_rate(max_nodes, step)
            fig = plot_growth_rate(nodes, times)
            st.plotly_chart(fig, use_container_width=True)

        st.success(f"Growth rate analysis completed for up to {max_nodes} nodes.")