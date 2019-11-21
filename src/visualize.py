#!/usr/bin/env python
import rospy
import numpy as np
from numpy import genfromtxt
import random
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib import style
import pdb
from math import cos,sin,radians

# plt.rcParams.update({'font.size': 14})
# import os
# from statistics import mean

# fig,(ax1,ax2,ax3,ax4) = plt.subplots(2,2)
# fig,(ax1) = plt.subplots(1,1)
fig, ax = plt.subplots()
count = 0
global_least_euclidian_distances = []
#ax1.set_title(r'Range VS Time')
#ani = 1
# global_waypoint_distance_values = []
# global_waypoint_count = 0 	#to see how any entries range values has and then plot only when new values come
# global_waypoints_mean_distance = 0

# def global_waypoint_dist_callback(distance):
# 	global global_waypoint_distance_values
# 	global_waypoint_distance_values.append(distance.range + random.randint(1,30))

def get_least_euclidian_distances(global_waypoints,pit_edges):
	least_euclidian_distances = []
	for i in range(global_waypoints.shape[0]):
		least_euclidian_distances.append(np.asscalar(np.min(np.linalg.norm(global_waypoints[i,:] - pit_edges, axis=1))))
	return least_euclidian_distances

def get_global_waypoints_data():
	pit_edges_file_name = "src/visualization/data/pit_edges.csv"
	global_waypoints_file_name = "src/visualization/data/global_waypoints.csv"
	global_waypoints = genfromtxt(global_waypoints_file_name, delimiter=',')
	pit_edges = genfromtxt(pit_edges_file_name, delimiter=',')
	least_euclidian_distances = get_least_euclidian_distances(global_waypoints,pit_edges)
	return least_euclidian_distances

def animate(frames):
	global ax
	# global ax2
	# global ax3
	# global global_waypoint_distance_values
	# global global_waypoint_count
	global count
	global global_least_euclidian_distances
	rospy.loginfo("In Animate \n")

	if(count==0):
		least_euclidian_distances = get_global_waypoints_data()	
		global_least_euclidian_distances = least_euclidian_distances
		print("Distances calculated")
		count+=1
	else:
		least_euclidian_distances = global_least_euclidian_distances

	ax.clear()
	average = sum(least_euclidian_distances) / len(least_euclidian_distances)
	x = np.arange(len(least_euclidian_distances))  # the label locations
	width = 0.35  # the width of the bars

	rects1 = ax.bar(x - width/2, least_euclidian_distances, width, label='')

	# Add some text for labels, title and custom x-axis tick labels, etc.
	ax.set_ylabel('Distance of global waypoints from pit edge (m)')
	ax.set_title('Distances of global waypoints from pit edge')
	ax.hlines(y=average, xmin=-1, xmax=len(x), linestyle='--', color='r')
	plt.text(-1*0.9, average*1.05, 'Mean: {:.2f}'.format(average))
	ax.set_xticks(x)
	ax.set_xticklabels(x)
	ax.legend()
	autolabel(rects1)
	fig.tight_layout()

	
	# if(len(global_waypoint_distance_values)>global_waypoint_count):
	# 	global_waypoint_count+=1 
    #     average = sum(global_waypoint_distance_values) / len(global_waypoint_distance_values)
	# 	# string_to_display_on_graph = 'Mean: ' + str(round(average,2))  #Add appropriate units
	# 	# ax1.clear()
	# 	# ax1.scatter(range_time_values, range_values,color='blue')
	# 	# ax1.annotate(string_to_display_on_graph,xy=(0.5, 0.9), xycoords="axes fraction")
	# 	#ax2.set_yticks(np.arange(min(range_values),max(range_values)+1))
	# 	#max value can also be plotted. max_value is being maintained

    #     x = np.arange(global_waypoint_count)  # the label locations
    #     width = 0.35  # the width of the bars

    #     rects1 = ax.bar(x - width/2, global_waypoint_distance_values, width, label='')

    #     # Add some text for labels, title and custom x-axis tick labels, etc.
    #     ax.set_ylabel('Distance of global waypoints from pit edge')
    #     ax.set_title('Distances of global waypoints from pit edge')
    #     ax.set_xticks(x)
    #     ax.set_xticklabels(x)
    #     ax.legend()
    #     autolabel(rects1)
    #     fig.tight_layout()


def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    global ax
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{0:.2f}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

# def set_axis_labels():
# 	global ax
# 	# global ax2
# 	# global ax3
# 	ax.set_ylabel('Range')
# 	ax1.set_xlabel('Time')
# 	# ax1.set_title(r'Range VS Time')
# 	# ax2.set_title(r'Bearing VS Time')
# 	# ax3.set_title(r'Rover Position VS Time')

if __name__ == '__main__':
	rospy.init_node('visualize', anonymous=True)
	# rospy.Subscriber("/global_waypoint_dist", Range, global_waypoint_dist_callback)
	rate = rospy.Rate(10)
	rospy.loginfo("In Main \n")
	ani = animation.FuncAnimation(fig,animate,frames = None,interval = 50)
	while not rospy.is_shutdown():
		plt.show()
		rate.sleep()
