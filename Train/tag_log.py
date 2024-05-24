import pandas as pd
import matplotlib.pyplot as plt
import glob

file_pattern = r'D:\Files\Projects\ESP_UWB\ESP_UWB_calib\Train\tag_log_3.csv'
files = glob.glob(file_pattern)

x_data = []
y_data = []
z_data = []

n=0
for file in files:
    data = pd.read_csv(file)
    x_data.append(list(data['x_coord']))
    y_data.append(list(data['y_coord']))
    z_data.append(list(data['z_coord']))
    n+=1


# Creating the 3D scatter plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
#ax = fig.add_subplot(111)

colors = ['b', 'g', 'r', 'c', 'b', 'y', 'k', 'orange', 'purple', 'pink']

for n in range(len(x_data)):
    ax.scatter(x_data[n], y_data[n], z_data[n], marker="o", s = 1, c = colors[n], label = f"Kolo {n}") 

#ax.scatter(x, y,  marker='o', s=2) 

#ax.set_xlabel('X Label')
#ax.set_ylabel('Y Label')
#ax.set_zlabel('Z Label')

ax.set_xlim(0, 6)
ax.set_ylim(0, 6)
ax.set_zlim(0, 6)

#ax.autoscale(enable = False)


plt.show()
