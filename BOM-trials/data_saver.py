# data_saver.py

import csv
import os

def save_to_csv(data, output_dir='output'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for key, items in data.items():
        if key == 'business_group':
            items = [items]  # Convert single dict to list for consistent processing

        filename = os.path.join(output_dir, f'{key}.csv')
        with open(filename, 'w', newline='') as csvfile:
            if items:
                fieldnames = items[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for item in items:
                    writer.writerow(item)
        print(f"Saved {filename}")