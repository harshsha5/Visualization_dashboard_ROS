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
from std_msgs.msg import Float32
import cv2

#=========================================================================================================================================

fig, (ax1,ax2) = plt.subplots(1,2)
counter = 0
g_rock_dist = []
g_rock_dist_count = 0
g_rock_dist_counter = 0
ROCK_DIST_THRESHOLD = 0.5
ROCK_DIST_PUBLISH_FREQ = 25

#==========================================================================================================================================

# def odom_callback(odom_data):			#Use the msg.flag to see if you need to keep publishing old message or use the new one
#     global counter
#     rospy.sleep(1)
#     curr_time = odom_data.header.stamp
#     pose = odom_data.pose.pose #  the x,y,z pose and quaternion orientation
#     counter= counter+1
#     print(counter, curr_time)
#     print (pose)

def rock_dist_callback(msg):			#Use the msg.flag to see if you need to keep publishing old message or use the new one
	global g_rock_dist_counter
	g_rock_dist_counter+=1
	if(g_rock_dist_counter%ROCK_DIST_PUBLISH_FREQ==0):
		g_rock_dist.append(msg.data)

def set_font_size(ax):
	for label in (ax.get_yticklabels()):
		label.set_fontname('Arial')
		label.set_fontsize(28)

def animate(frames):
	global ax1
	global ax2
	global g_rock_dist_count
	rospy.loginfo("In Animate \n")

	if(g_rock_dist_count<len(g_rock_dist)):
		g_rock_dist_count +=1
		plot_len = min(g_rock_dist_count,len(g_rock_dist))
		ax2.clear()
		x = np.arange(plot_len)
		fail_count = len([i for i in g_rock_dist[0:plot_len] if i > ROCK_DIST_THRESHOLD]) 
		ax2.plot(x, g_rock_dist[0:plot_len])
		ax2.set_ylabel('Distance of rover from nearest rock (m)',fontsize=28)
		ax2.set_xlabel('Time index')
		ax2.set_title('Obstacles Avoidance Test',fontsize=28)
		set_font_size(ax2)

		# place a text box in upper left in axes coords
		metric = (g_rock_dist_count-fail_count)*100/g_rock_dist_count
		textstr = '% of waypoints within threshold: {:.2f}'.format(metric)
		if(metric>0.8):
			props = dict(boxstyle='round', facecolor='lightgreen', alpha=0.5)
		else:
			props = dict(boxstyle='round', facecolor='darksalmon', alpha=0.5)
		ax2.text(0.05, 0.95, textstr, transform=ax2.transAxes, fontsize=22,verticalalignment='top', bbox=props, weight='bold')
		ax2.set_xticks(x)
		ax2.set_xticklabels(x)
		ax2.get_xaxis().set_ticks([])
		ax2.legend()


if __name__ == '__main__':
	rospy.init_node('visualize_test1', anonymous=True)
	# rospy.Subscriber("/odometry_ground_truth",Odometry,odom_callback)
	rospy.Subscriber("/min_rock_dist",Float32,rock_dist_callback)
	rate = rospy.Rate(10)
	rospy.loginfo("In Main \n")
	ani = animation.FuncAnimation(fig,animate,frames = None,interval = 10)
	while not rospy.is_shutdown():
		plt.show()
		rate.sleep()
