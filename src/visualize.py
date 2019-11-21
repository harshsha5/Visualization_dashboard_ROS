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
from cv_bridge import CvBridge
from sensor_msgs.msg import Image

# plt.rcParams.update({'font.size': 14})
# import os
# from statistics import mean

# fig,(ax1,ax2,ax3,ax4) = plt.subplots(2,2)
# fig,(ax1) = plt.subplots(1,1)
fig, (ax1,ax2) = plt.subplots(1,2)
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

def pit_image_callback(msg):			#Use the msg.flag to see if you need to keep publishing old message or use the new one
	rospy.loginfo('Image received...')
	image = CvBridge().imgmsg_to_cv2(msg)
	ax2.imshow(image)
	ax2.axis('off')

def get_least_euclidian_distances(global_waypoints,pit_edges):
	least_euclidian_distances = []
	for i in range(global_waypoints.shape[0]):
		least_euclidian_distances.append(np.asscalar(np.min(np.linalg.norm(global_waypoints[i,:] - pit_edges, axis=1))))
	return least_euclidian_distances

def get_global_waypoints_data():
	pit_edges_file_name = "src/visualization/data/pit_edges.csv"
	global_waypoints_file_name = "src/visualization/data/global_waypoints.csv"
	global_waypoints = genfromtxt(global_waypoints_file_name, delimiter=',')		#TODO: Resolution transform these global waypoints
	pit_edges = genfromtxt(pit_edges_file_name, delimiter=',')
	least_euclidian_distances = get_least_euclidian_distances(global_waypoints,pit_edges)
	return least_euclidian_distances

def animate(frames):
	global ax1
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

	ax1.clear()
	average = sum(least_euclidian_distances) / len(least_euclidian_distances)
	x = np.arange(len(least_euclidian_distances))  # the label locations
	width = 0.35  # the width of the bars

	rects1 = ax1.bar(x - width/2, least_euclidian_distances, width, label='')

	# Add some text for labels, title and custom x-axis tick labels, etc.
	ax1.set_ylabel('Distance of global waypoints from pit edge (m)')
	ax1.set_title('Distances of global waypoints from pit edge')
	ax1.hlines(y=average, xmin=-1, xmax=len(x), linestyle='--', color='r')
	ax1.text(-1*0.9, average*1.02, 'Mean: {:.2f}'.format(average))
	ax1.set_xticks(x)
	ax1.set_xticklabels(x)
	ax1.legend()
	autolabel(rects1,ax1)

	# image_path = "src/visualization/data/index.jpeg"
	# img = plt.imread(image_path)
	# ax2.imshow(img)
	# ax2.axis('off')

	fig.tight_layout()

def autolabel(rects,ax):
    """Attach a text label above each bar in *rects*, displaying its height."""
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
	rospy.Subscriber("/apnapioneer3at/MultiSense_S21_meta_camera/image",Image,pit_image_callback)
	rate = rospy.Rate(50)
	rospy.loginfo("In Main \n")
	ani = animation.FuncAnimation(fig,animate,frames = None,interval = 50)
	while not rospy.is_shutdown():
		plt.show()
		rate.sleep()
