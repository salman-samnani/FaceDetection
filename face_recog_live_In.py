# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 00:07:44 2020

@author: OMER-EPG-UK
"""


import logging
import pickle
import numpy as np
import tensorflow as tf
from tensorflow.python.platform import gfile
from tensorflow.python.framework import ops
import cv2

from scipy import misc
import detect_face

import os
import time
from datetime import date


logger = logging.getLogger(__name__)


def write_error_log(data):
	print ("---------- LOGGING Error-------------")
	att_time = time.strftime("%H:%M:%S")
	att_date = date.today()
	#print (att_date)
	#print (att_time)
	currentDT = str(att_date) + ' ' +str(att_time)
	print(currentDT)
	f = open('error_log.txt','a')
	f.write(str(data) +','+ str(currentDT)+'---TimeStamp : '  + '\n')
	f.close()



def rotate_bound(image, angle):
	# grab the dimensions of the image and then determine the
	# center
	(h, w) = image.shape[:2]
	(cX, cY) = (w // 2, h // 2)

	# grab the rotation matrix (applying the negative of the
	# angle to rotate clockwise), then grab the sine and cosine
	# (i.e., the rotation components of the matrix)
	M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
	cos = np.abs(M[0, 0])
	sin = np.abs(M[0, 1])

	# compute the new bounding dimensions of the image
	nW = int((h * sin) + (w * cos))
	nH = int((h * cos) + (w * sin))

	# adjust the rotation matrix to take into account translation
	M[0, 2] += (nW / 2) - cX
	M[1, 2] += (nH / 2) - cY

	# perform the actual rotation and return the image
	return cv2.warpAffine(image, M, (nW, nH))


class ImageClass():
	def __init__(self, name, image_paths):
		self.name = name
		self.image_paths = image_paths

	def __str__(self):
		return self.name + ', ' + str(len(self.image_paths)) + ' images'

	def __len__(self):
		return len(self.image_paths)
	
folder = "images_out"
folder_2 = "images_in"

face_detected = False

def main():
	global face_detected
	
	model_path = "models/20170511-185253.pb"
	# classifier_output_path = "/mnt/softwares/acv_project_code/Code/classifier_rf1_team.pkl"
	classifier_output_path = "models/classifier_rf4.pkl"
	#classifier_output_path = "/mnt/softwares/acv_project_code/Code/classfier_path/classifier_svm.pkl"
	
	with gfile.FastGFile(model_path, 'rb') as f:
		graph_def = tf.GraphDef()
		graph_def.ParseFromString(f.read())
		tf.import_graph_def(graph_def, name='')
	images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
	embedding_layer = tf.get_default_graph().get_tensor_by_name("embeddings:0")
	phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")
	gpu_memory_fraction = 0.5
	
	with tf.Graph().as_default():
		
		gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=gpu_memory_fraction)
		
		sess1 = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options, log_device_placement=False))
		
		# sess1 = tf.Session(config=tf.ConfigProto(device_count = {'GPU': 0}))
		with sess1.as_default():
			
			pnet, rnet, onet = detect_face.create_mtcnn(sess1, None)
			
	model, class_names = pickle.load(open(classifier_output_path, 'rb'), encoding='latin1')

	#cap = cv2.VideoCapture(0)
	#cap = cv2.VideoCapture("rtsp://admin:Epagingadmin@10.194.2.141:554/");
	#rtsp://admin:Epagingadmin123@10.194.2.141:554/cam/realmonitor?channel=1&subtype=1 
	cap_2 = cv2.VideoCapture("rtsp://admin:Epagingadmin@10.194.2.51:554/")
	# cap = cv2.VideoCapture('/home/lokender/Downloads/orig_faces/videos/nayeem.mp4')
	# cap = cv2.VideoCapture('/home/lokender/Downloads/orig_faces/videos/lokender.mp4')
	fno = 0
	det_name = []
	det_prob =[]
	bbs = []
	i = 0
	while (~(cv2.waitKey(1) & 0xFF == ord('q'))):
		#print(time.strftime("%H:%M:%S"))
		'''
		# image2 = cv2.imread("/home/lokender/Downloads/T1/both/IMG_20171115_150720.jpg")
		# image2.set_shape((480, 640, 3))
		# image2= cv2.resize(image2, (640,480))
		ret, image1 = cap.read()
		image2 = cv2.resize(image1, (320, 240))
					
		minsize = 20  # minimum size of face
		threshold = [0.6, 0.7, 0.7]  # three steps's threshold
		factor = 0.709  # scale factor

		img = image2[:, :, 0:3]
		print('it - 1')

		bounding_boxes, _ = detect_face.detect_face(img, minsize, pnet, rnet, onet, threshold, factor)
		print('it - 2')
		nrof_faces = bounding_boxes.shape[0]
		print(nrof_faces)
		
		if nrof_faces == 1:
			
			path = os.path.join(os.getcwd(),  folder, str(i)+'.jpg')
			cv2.imwrite(path, image1)
			i = i+1
			face_detected = True
			print("taking first imagae_" + str(i))
				
		cv2.imshow('fr', image2)
		fno = fno + 1
		
		'''
		 # image2 = cv2.imread("/home/lokender/Downloads/T1/both/IMG_20171115_150720.jpg")
		# image2.set_shape((480, 640, 3))
		# image2= cv2.resize(image2, (640,480))
		
		ret, image3 = cap_2.read()
		
		image4 = cv2.resize(image3, (600, 400))
					
		minsize = 20  # minimum size of face
		threshold = [0.6, 0.7, 0.7]  # three steps's threshold
		factor = 0.709  # scale factor

		img = image4[:, :, 0:3]
		

		bounding_boxes, _ = detect_face.detect_face(img, minsize, pnet, rnet, onet, threshold, factor)
		
		nrof_faces = bounding_boxes.shape[0]
		#print(nrof_faces)
		
		if nrof_faces == 1:
			
			path = os.path.join(os.getcwd(),  folder_2, str(i)+'.jpg')
			cv2.imwrite(path, image3)
			i = i+1
			face_detected = True
			print("taking first imagae_" + str(i))
				
		#cv2.resize(image4,(600,400))
		cv2.imshow('In Camera Live Feed', image4)
		fno = fno + 1
		
	#cap.release()
	cap_2.release()
	cv2.destroyAllWindows()


if __name__ == '__main__':
	while True:
		try:
			main()
		except:    
			write_error_log('Exception Occured In cam')
			print("Exception-----")