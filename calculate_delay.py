import os
import csv
import random
import math
from typing import Dict

baseDelay = 513*10**(-9)   #512ns
perturbation = 0.2 * 10**(-9) #2ns

def distanceToClk(distance: float) -> float:
    timestep_res = 15.650040064103* 10**(-12)
    light_speed = 299702547

    return (distance / light_speed) / timestep_res

def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def timeToClock(time: float) -> float:
    timestep_res = 15.650040064103* 10**(-12)

    return time / timestep_res

# Doesnt really work the math is bad

class rndDelay:

    def __init__(self, random_val_clk: float, distance_m: float, measured_clk: Dict[str, float]) -> None:
        self.tag_delay_clk = random_val_clk
        self.act_dist_m = distance_m
        self.measured_TOF_clk = measured_clk
        self.distances_triangle: Dict = {"11a1": 0.127, "12a2": 0.128, "13a3": 0.139, "14a4": 0.141, "15a5": 0.124}

        self.act_distances_m = dict()
        self.actual_TOF_clk = dict()
        self.deltaTOF = dict()
        self.anchor_delay_clk = dict()
        self.candidate_TOF_clk = dict()
        self.candidate_deltaTOF = dict()

        for key in self.distances_triangle.keys():

            self.act_distances_m[key] = math.sqrt(self.distances_triangle[key]**2 + self.act_dist_m**2)
            self.actual_TOF_clk[key] = distanceToClk(self.act_distances_m[key])

            self.deltaTOF[key] = abs(self.actual_TOF_clk[key] - self.measured_TOF_clk[key])
            self.anchor_delay_clk[key] = self.deltaTOF[key] - self.tag_delay_clk

            self.candidate_TOF_clk[key] = (-4*self.anchor_delay_clk[key] + -4 * self.tag_delay_clk + 4* self.measured_TOF_clk[key])/4
            self.candidate_deltaTOF[key] = abs(self.candidate_TOF_clk[key] - self.actual_TOF_clk[key])

        self.totalDelta = float()

        for key in  self.candidate_deltaTOF.keys():
            self.totalDelta += self.candidate_deltaTOF[key]

    def getTotalDelta(self) -> float:
        return self.totalDelta

    def __lt__(self, value):
        return self.totalDelta < value.getTotalDelta()




distances = dict()
# Define the directory path
directory = r'D:\Files\Projects\ESP_UWB\ESP_UWB_calib'

distances_path = os.path.join(directory, "distances.csv")

with open(distances_path, 'r', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    for row in reader:
        if row[0].isnumeric():
            distances[int(row[0])] = float(row[1])

# Iterate over the directory and its subdirectories
for root, dirs, files in os.walk(directory):
    for file in files:

        if file == 'averages.csv':

            file_path = os.path.join(root, file)
            meassurment = int(os.path.basename(root))

            with open(file_path, 'r', newline='') as csvfile:
                reader = csv.reader(csvfile)
                TOF_meassured = dict()
                for row in reader:
                    if is_float(row[3]):
                        TOF_meassured[row[0]] = float(row[3])
            
            rndDistribution = []
            for i in range(1000):
                rndValue = random.normalvariate(baseDelay, perturbation)/2
                rndValue_clk = timeToClock(rndValue)

                rndDistribution.append(rndDelay(rndValue_clk, distances[meassurment], TOF_meassured))

            sorted_rnd_delay = sorted(rndDistribution)

            


                

            
