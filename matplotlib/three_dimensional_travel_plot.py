import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdate
import numpy as np
from datetime import time as ti1
from datetime import datetime as dt
import calendar

reference_time = dt.fromisoformat('2024-10-01T00:00:00Z')

# Create a figure and 3D axes
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# arr_time = dt.fromisoformat('2024-10-01T23:11:00Z')
# point = dt.strftime(arr_time, "%H:%M")
# timedelta1 = arr_time - reference_time
# timedelta1_in_hours = timedelta1.total_seconds() / 3600
# IMPLEMENTATION 3: change the time array into 3: train, bus, flight


def return_epoch_times_list(arr_time_array) -> list[int]:
    list_of_epoch_times = []
    for item in arr_time_array:
        years_portion = int(item[:4])
        months_portion = int(item[5:7])
        days_portion = int(item[8:10])
        hours_portion = int(item[11:13])
        minutes_portion = int(item[14:16])
        converted_datetime = dt(years_portion, months_portion, days_portion, hours_portion, minutes_portion)
        list_of_epoch_times.append(calendar.timegm(converted_datetime.timetuple()))
    return list_of_epoch_times

arr_time_array = ['2024-10-02T00:20:00Z', '2024-10-01T22:50:00Z', '2024-10-01T23:50:00Z', '2024-10-02T01:35:00Z',
                  '2024-10-02T00:25:00Z', '2024-10-02T01:35:00Z', '2024-10-02T00:07:00Z', '2024-10-01T23:11:00Z',
                  '2024-10-01T22:39:00Z', '2024-10-01T23:05:00Z', '2024-10-01T22:38:00Z',
                  '2024-10-01T22:40:00Z', '2024-10-01T21:35:00Z', '2024-10-02T01:36:00Z', '2024-10-02T01:37:00Z',
                  '2024-10-01T23:41:00Z', '2024-10-01T23:38:00Z', '2024-10-01T21:13:00Z', '2024-10-01T22:50:00Z']
list_of_x_vals = []
list_of_epoch_times = []

# okay, transform this.
arr_train_times = ['2024-10-01T22:26:00Z', '2024-10-01T22:52:00Z', '2024-10-02T00:40:00Z', '2024-10-02T01:05:00Z']
arr_train_costs = [103, 138, 60, 38]
arr_train_travel_time = [6.07, 5.98, 6.12, 6.00]
arr_plane_times = ['2024-10-02T00:07:00Z', '2024-10-01T23:11:00Z', '2024-10-01T22:39:00Z', '2024-10-01T23:05:00Z', 
                   '2024-10-01T22:38:00Z', '2024-10-01T22:40:00Z', '2024-10-01T21:35:00Z', '2024-10-02T01:36:00Z', 
                   '2024-10-02T01:37:00Z', '2024-10-01T23:41:00Z', '2024-10-01T23:38:00Z', '2024-10-01T21:13:00Z']
arr_plane_costs = [30, 149, 158, 164, 149, 149, 134, 149, 149, 149, 149, 134]
arr_plane_travel_time = [4.62, 4.6, 4.73, 4.6, 4.47, 4.67, 4.58, 4.85, 4.88, 4.93, 4.9, 4.97]
arr_bus_times =  ['2024-10-02T00:20:00Z', '2024-10-01T22:50:00Z', '2024-10-01T23:50:00Z', '2024-10-02T01:35:00Z',
                  '2024-10-02T00:25:00Z', '2024-10-02T01:35:00Z', '2024-10-01T22:50:00Z']
arr_bus_costs = [33, 29, 36, 36, 33, 33, 35]
arr_bus_travel_time = [5.83, 5.83, 6.58, 6.08, 6.75, 6.33, 6.33]

arr_epoch_train = return_epoch_times_list(arr_train_times)
arr_epoch_plane = return_epoch_times_list(arr_plane_times)
arr_epoch_bus = return_epoch_times_list(arr_bus_times)

'''
for item in arr_time_array:
    timedelta1 = dt.fromisoformat(item) - reference_time
    timedelta1_in_hours = timedelta1.total_seconds() / 3600
    list_of_x_vals.append(timedelta1_in_hours)
    # print(timedelta1_in_hours)
'''

master_list_of_epoch_times = []

''' implementation 1:
# datetime objects
for item in arr_time_array:
    years_portion = int(item[:4])
    months_portion = int(item[5:7])
    days_portion = int(item[8:10])
    hours_portion = int(item[11:13])
    minutes_portion = int(item[14:16])
    converted_datetime = dt(years_portion, months_portion, days_portion, hours_portion, minutes_portion)
    list_of_x_vals.append(converted_datetime)
    master_list_of_epoch_times.append(calendar.timegm(converted_datetime.timetuple()))
'''

master_list_of_epoch_times = arr_epoch_train + arr_epoch_plane + arr_epoch_bus

# Generate sample data (x=arrival time, y=cost, z=travel time)
list_of_y_vals = [33, 29, 36, 36, 33, 33, 30, 149, 158, 164, 149, 149, 134, 149, 149, 149, 149, 134, 35]
list_of_z_vals = [5.83, 5.83, 6.58, 6.08, 6.75, 6.33, 4.62, 4.6, 4.73, 4.6, 4.47, 4.67, 4.58, 4.85, 4.88, 4.93, 4.9, 4.97, 6.33]


# Create the 3D surface plot
fig, ax = plt.subplots(subplot_kw=dict(projection='3d'))
# dates = matplotlib.dates.date2num(list_of_x_vals) # implmentation 1 used dates
# ax.stem(list_of_x_vals, list_of_y_vals, list_of_z_vals, basefmt=" ")

# markerline, stemlines, baseline = ax.stem(master_list_of_epoch_times, list_of_y_vals, list_of_z_vals, basefmt=" ", markerfmt="D")
markerline, stemlines, baseline = ax.stem(arr_epoch_train, arr_train_costs, arr_train_travel_time, linefmt="C1-", basefmt=" ", markerfmt="C1D", label="Train")
markerline, stemlines, baseline = ax.stem(arr_epoch_plane, arr_plane_costs, arr_plane_travel_time, linefmt="C0-", basefmt=" ", markerfmt="C0X", label="Plane")
markerline, stemlines, baseline = ax.stem(arr_epoch_bus, arr_bus_costs, arr_bus_travel_time, linefmt="C3-", basefmt=" ", markerfmt="C3^", label="Bus")

plt.gca().get_yaxis().set_tick_params(which="minor", pad=5)
plt.gca().get_yaxis().set_tick_params(which="major", pad=5)

# IMPLEMENTATION 1
# was: markerline, stemlines, baseline = ax.stem(dates, list_of_y_vals, list_of_z_vals, basefmt=" ", markerfmt="D")

# date_fmt = '%d %H:%M'

# Use a DateFormatter to set the data to the correct format.
# date_formatter = mdate.DateFormatter(date_fmt)
# ax.xaxis.set_major_formatter(date_formatter)

# Set labels and title
ax.set_ylabel('Price')
ax.set_zlabel('Travel Time (hrs)')
ax.set_xlabel('ETA Home')
ax.legend(loc='upper center', ncol=3)
plt.title('3D Plot of Price vs. Travel Time vs. ETA')
integer_yticks = [int(x) for x in ax.get_yticks()]
ax.set_yticks(integer_yticks)
ax.set_yticklabels(integer_yticks, verticalalignment='baseline', horizontalalignment='left')

# IMPLEMENTATION 2
plt.xticks(ticks=np.arange(min(master_list_of_epoch_times), max(master_list_of_epoch_times)+3600, 3600), 
           labels=['21:00', '22:00', '23:00', '0:00', '1:00', '2:00'])
# plt.yticks(ticks=[20, 40, 60, 80, 100, 120, 140, 160], labels=['20', '40', '60', '80', '100', '120', '140', '160'])

# Show the plot
plt.show()
