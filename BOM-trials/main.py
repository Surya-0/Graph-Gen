# main.py

from data_generator import DataGenerator
from data_saver import save_to_csv,save_graph
from graph_visualizer import main as visualize_graph

def main():
    # Generate data
    print("Generating supply chain data...")
    generator = DataGenerator()
    generator.generate_data()
    data = generator.get_data()

    # Save data to CSV files
    print("Saving data to CSV files...")
    save_to_csv(data)

    # Save graph
    print("Saving graph...")
    save_graph(data)

    # Visualize the graph
    print("Visualizing graph...")
    visualize_graph()

    # # Analyze the graph
    # print("Analyzing graph...")
    # analyze_graph()

    print("Process completed successfully.")

if __name__ == "__main__":
    main()