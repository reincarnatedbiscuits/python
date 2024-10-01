import matplotlib.pyplot as plt
import numpy as np
from datetime import time as ti1
from datetime import datetime as dt

reference_time = dt.fromisoformat('2024-09-30T00:00:00Z')

# Create a figure and 3D axes
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

arr_time = dt.fromisoformat('2024-09-30T23:11:00Z')
point = dt.strftime(arr_time, "%H:%M")
timedelta1 = arr_time - reference_time
timedelta1_in_hours = timedelta1.total_seconds() / 3600

arr_time_array = ['2024-10-01T00:20:00Z', '2024-09-30T22:50:00Z', '2024-09-30T23:50:00Z', '2024-10-01T01:35:00Z',
                  '2024-10-01T00:25:00Z', '2024-10-01T01:35:00Z', '2024-10-01T00:07:00Z', '2024-09-30T23:11:00Z',
                  '2024-09-30T22:39:00Z', '2024-09-30T23:05:00Z', '2024-09-30T22:38:00Z',
                  '2024-09-30T22:40:00Z', '2024-09-30T21:35:00Z', '2024-10-01T01:36:00Z', '2024-10-01T01:37:00Z',
                  '2024-09-30T23:41:00Z', '2024-09-30T23:38:00Z', '2024-09-30T21:13:00Z', '2024-09-30T22:50:00Z']
list_of_x_vals = []

for item in arr_time_array:
    timedelta1 = dt.fromisoformat(item) - reference_time
    timedelta1_in_hours = timedelta1.total_seconds() / 3600
    list_of_x_vals.append(timedelta1_in_hours)
    # print(timedelta1_in_hours)

# Generate sample data (X=cost, y=travel time, z=arrival time)
list_of_y_vals = [33, 29, 36, 36, 33, 33, 30, 149, 158, 164, 149, 149, 134, 149, 149, 149, 149, 134, 35]
list_of_z_vals = [5.83, 5.83, 6.58, 6.08, 6.75, 6.33, 4.62, 4.6, 4.73, 4.6, 4.47, 4.67, 4.58, 4.85, 4.88, 4.93, 4.9, 4.97, 6.33]

# Create the 3D surface plot
fig, ax = plt.subplots(subplot_kw=dict(projection='3d'))
ax.stem(list_of_x_vals, list_of_y_vals, list_of_z_vals, basefmt=" ")

# Set labels and title
ax.set_ylabel('Price')
ax.set_zlabel('Travel Time (hrs)')
ax.set_xlabel('ETA Home')
plt.title('3D Plot')

# for line in ax.lines:
#      line.set_marker('none')

# Show the plot
plt.show()
