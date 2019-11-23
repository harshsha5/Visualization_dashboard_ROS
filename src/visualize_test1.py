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
from nav_msgs.msg import Odometry
import cv2

#=========================================================================================================================================

fig, (ax1,ax2) = plt.subplots(1,2)
counter = 0

#==========================================================================================================================================

def odom_callback(odom_data):			#Use the msg.flag to see if you need to keep publishing old message or use the new one
    global counter
    rospy.sleep(1)
    curr_time = odom_data.header.stamp
    pose = odom_data.pose.pose #  the x,y,z pose and quaternion orientation
    counter= counter+1
    print(counter, curr_time)
    print (pose)

def set_font_size(ax):
	for label in (ax.get_xticklabels() + ax.get_yticklabels()):
		label.set_fontname('Arial')
		label.set_fontsize(28)

# def animate(frames):
# 	global ax1
# 	# global ax2
# 	# global ax3
# 	# global global_waypoint_distance_values
# 	# global global_waypoint_count
# 	global g_number_of_waypoints_within_threshold
# 	global index
# 	global inF
# 	global count
# 	global global_least_euclidian_distances
# 	global global_pit_edges
# 	rospy.loginfo("In Animate \n")

# 	if(count==0):
# 		least_euclidian_distances,pit_edges,number_of_waypoints_within_threshold = get_global_waypoints_data()	
# 		global_least_euclidian_distances = least_euclidian_distances
# 		g_number_of_waypoints_within_threshold = number_of_waypoints_within_threshold
# 		global_pit_edges = pit_edges
# 		print("Distances calculated")
# 		count+=1
# 	else:
# 		least_euclidian_distances = global_least_euclidian_distances
# 		number_of_waypoints_within_threshold = g_number_of_waypoints_within_threshold

# 	ax1.clear()
# 	average = sum(least_euclidian_distances) / len(least_euclidian_distances)
# 	x = np.arange(len(least_euclidian_distances))  # the label locations
# 	width = 0.35  # the width of the bars

# 	rects1 = ax1.bar(x - width/2, least_euclidian_distances, width, label='')

# 	# _, ymax = ax1.get_ylim()
# 	ax1.set_ylabel('Distance of global waypoints from pit edge (m)',fontsize=28)
# 	ax1.set_xlabel('Global Waypoint number',fontsize=28)
# 	set_font_size(ax1)
# 	ax1.set_title('Distances of global waypoints from pit edge',fontsize=28)
# 	ax1.hlines(y=average, xmin=-1, xmax=len(x), linestyle='--', color='r')
# 	ax1.text(-1*0.9, average*1.02, 'Mean: {:.2f}'.format(average),fontsize=28)

# 	# place a text box in upper left in axes coords
# 	textstr = '% of waypoints within threshold: {:.2f}'.format(number_of_waypoints_within_threshold*100/len(least_euclidian_distances))
# 	props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
# 	ax1.text(0.05, 0.95, textstr, transform=ax1.transAxes, fontsize=14,
#         verticalalignment='top', bbox=props, weight='bold')
# 	ax1.set_xticks(x)
# 	ax1.set_xticklabels(x)
# 	ax1.legend()
# 	autolabel(rects1,ax1)
# 	# fig.tight_layout()

def autolabel(rects,ax):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{0:.2f}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom',size=15)


if __name__ == '__main__':
	rospy.init_node('visualize_test1', anonymous=True)
	rospy.Subscriber("/odometry_ground_truth",Odometry,odom_callback)
	rate = rospy.Rate(10)
	rospy.loginfo("In Main \n")
	# ani = animation.FuncAnimation(fig,animate,frames = None,interval = 10)
	while not rospy.is_shutdown():
		plt.show()
		rate.sleep()
