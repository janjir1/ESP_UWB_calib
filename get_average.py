import os
import csv
import statistics

directory = r'D:\Files\Projects\ESP_UWB\ESP_UWB_calib\Meassurment 2'

def get_average(data: list, name: str) -> dict:

    all_distances = []
    first_row = True

    for row in data:

        if first_row:
            first_row = False
            continue

        if len(row) > 6:
            all_distances.append(float(row[6]))

    average = dict()
    average["Name"] = name[-19:-15]

    sorted_disances = sorted(all_distances)
    n = len(sorted_disances)

    if n % 2 == 0:
        # If the list has an even number of elements, take the average of the middle two
        average["TOF"] = sorted_disances[n // 2 - 1]
    else:
        # If the list has an odd number of elements, return the middle element
        average["TOF"] = sorted_disances[n // 2]

    first_row = True
    for row in data:

        if first_row:
            first_row = False
            continue

        if len(row) > 6:
            if  average["TOF"] == float(row[6]):

                average["RX"] = float(row[4])
                average["FP"] = float(row[5])
                average["dist"] = float(row[7])

    return average

def saveAverage(averages: list, root: str) -> None:
    path = os.path.join(root, "averages.csv")
    with open(path, 'w', newline='') as csv_file:
    # Create a CSV writer
        writer = csv.DictWriter(csv_file, fieldnames=averages[0].keys())
        
        # Write the updated data back to the file
        writer.writeheader()
        
        writer.writerows(averages)

#forbidden: list = ["_claculated.csv", "averages.csv", "delay.csv", "distances.csv"]

# Walk through the directory structure
for root, dirs, files in os.walk(directory):

    averages = []

    for file in files:

        if file.endswith('_claculated.csv'):
            
            #if not any(file.endswith(end) for end in forbidden):
                # Get the full path of the CSV file
            file_path = os.path.join(root, file)
            print(file)
            
            
            # Open the CSV file
            with open(file_path, 'r') as csv_file:
                # Create a CSV reader
                csv_reader = csv.reader(csv_file)
                data = list(csv_reader)
                
                averages.append(get_average(data, file))

    if averages:
            saveAverage(averages, root)