import pandas as pd
import matplotlib.pyplot as plt
import glob

file_pattern = r'C:\Users\Janjiri\Desktop\Soubory\ESP_UWB\ESP_UWB_calib\Train\tag_log_3.csv'
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


colors = ['b', 'g', 'r', 'c', 'm', 'y', 'orange', 'k', 'purple', 'pink']

for n in range(len(x_data)):
    ax.scatter(x_data[n], y_data[n], z_data[n], marker="x", s = 0.1, c = "b", label = f"Částice")

anchors = {"11a1": [0.0, 0.0, 0.51], "12a2": [4.6, 0.1, 0.23], "13a3": [5.14, 3.3, 0.5], "14a4": [0.7, 3.34, 0.2], "15a5": [2.83, 2.47, 1.39]}

n=len(x_data)
for key in anchors:
    ax.scatter(anchors[key][0], anchors[key][1], anchors[key][2], marker="o", c=colors[n], s=30,  label = f"Anchor {key}")
    n+=1

plt.legend()

#("11a1", [0.0, 0.0, 0.51])
#("12a2", [4.6, 0.1, 0.23])
#("13a3", [5.14, 3.3, 0.5])
#("14a4", [0.7, 3.34, 0.2])
#("15a5", [2.83, 2.47, 1.39])

#ax.scatter(x, y,  marker='o', s=2) 

ax.set_xlabel('X [m]')
ax.set_ylabel('Y [m]')
ax.set_zlabel('Z [m]')

ax.set_xlim(0, 6)
ax.set_ylim(0, 6)
ax.set_zlim(0, 6)

plt.tight_layout()

#ax.autoscale(enable = False)


plt.show()
