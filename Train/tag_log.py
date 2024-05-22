import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Load the data from the CSV file
data = pd.read_csv(r'D:\Files\Projects\ESP_UWB\ESP_UWB_calib\Train\tag_log_4.csv')

# Extracting the x, y, z coordinates
x = data['x_coord']
y = data['y_coord']
z = data['z_coord']

# Creating the 3D scatter plot
fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')
ax = fig.add_subplot(111)

#ax.scatter(x, y, z, marker='o', s=2) 
ax.scatter(x, y,  marker='o', s=2) 

#ax.set_xlabel('X Label')
#ax.set_ylabel('Y Label')
#ax.set_zlabel('Z Label')

ax.set_xlim(-1, 7)
ax.set_ylim(-1, 7)
#ax.set_zlim(0, 6)

#ax.autoscale(enable = False)


plt.show()
