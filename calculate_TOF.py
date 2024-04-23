import os
import csv
import statistics
import re


# Define the directory path
directory = r'D:\Files\Projects\ESP_UWB\ESP_UWB_calib'

def wrap(number: float, max_value = int) -> float:
    if number < 0:
        number = number + max_value + 1

    return number

max_time = 1099511627775

def calulate_distance(clk_tof: int) -> int:
    timestep_res = 15.650040064103* 10**(-12)
    light_speed = 299702547

    return clk_tof * timestep_res* light_speed

def calculateTOF(data: list, name: str) -> dict:
    message_num = None
    POLL = None
    POLL_ACK = None
    RANGE = None

    RXavg = []
    FPavg = []
    distAvg = []
    TOFAvg = []

    for row in data:

        if not row[0].isnumeric():
            row.append("TOF_CLK")
            row.append("distance")

        if row[1] == "POLL" and row[0].isnumeric():
            message_num = row[0]
            POLL = [int(row[2]), int(row[3])]
            RXavg.append(float(row[4]))
            FPavg.append(float(row[5]))

        elif row[0] == message_num:  

            if row[1] == "POLL_ACK" :
                POLL_ACK= [int(row[2]), int(row[3])]
                RXavg.append(float(row[4]))
                FPavg.append(float(row[5]))

            elif row[1] == "RANGE" :
                RANGE = [int(row[2]), int(row[3])]
                RXavg.append(float(row[4]))
                FPavg.append(float(row[5]))

            if  POLL is not None and POLL_ACK is not None and RANGE is not None:
                round1 = wrap(POLL_ACK[1] - POLL[0], max_time)
                reply1 = wrap(POLL_ACK[0] - POLL[1], max_time)
                round2 = wrap(RANGE[1] - POLL_ACK[0], max_time)
                reply2 = wrap(RANGE[0] - POLL_ACK[1], max_time)

                clk_TOF = wrap((round1 * round2 - reply1 * reply2)/(round1 + reply1 + round2 + reply2), max_time)
                row.append(clk_TOF)
                TOFAvg.append(clk_TOF)

                distance = calulate_distance(clk_TOF)
                row.append(distance)
                distAvg.append(distance)

                POLL = None
                POLL_ACK = None
                RANGE = None

    with open(file_path[:-4] + "_claculated.csv", 'w', newline='') as csv_file:
        # Create a CSV writer
        csv_writer = csv.writer(csv_file)
        
        # Write the updated data back to the file
        csv_writer.writerows(data)

    average = dict()
    average["Name"] = name[-8:-4]
    average["RX"] = statistics.median(RXavg)
    average["FP"] = statistics.median(FPavg)
    average["TOF"] = statistics.median(TOFAvg)
    average["dist"] = statistics.median(distAvg)
    return average
    

def saveAverage(averages: list, root: str) -> None:
    path = os.path.join(root, "averages.csv")
    with open(path, 'w', newline='') as csv_file:
    # Create a CSV writer
        writer = csv.DictWriter(csv_file, fieldnames=averages[0].keys())
        
        # Write the updated data back to the file
        writer.writeheader()
        
        writer.writerows(averages)
    

forbidden: list = ["_claculated.csv", "averages.csv"]

# Walk through the directory structure
for root, dirs, files in os.walk(directory):

    averages = []

    for file in files:

        if file.endswith('.csv'):
            
            if not any(file.endswith(end) for end in forbidden):
                # Get the full path of the CSV file
                file_path = os.path.join(root, file)
                print(file)
                
                
                # Open the CSV file
                with open(file_path, 'r') as csv_file:
                    # Create a CSV reader
                    csv_reader = csv.reader(csv_file)
                    data = list(csv_reader)
                    
                    averages.append(calculateTOF(data, file))

    if averages:
        saveAverage(averages, root)




                            


