# main.py

from data_generator import DataGenerator
from data_saver import save_to_csv

def main():
    # Generate data
    generator = DataGenerator()
    generator.generate_data()
    data = generator.get_data()

    # Save data to CSV files
    save_to_csv(data)

if __name__ == "__main__":
    main()