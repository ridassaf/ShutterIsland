import os
import sys
import tensorflow as tf

path = sys.argv[1]


# Loads label file, strips off carriage return
label_lines = [line.rstrip() for line 
                   in tf.gfile.GFile("../images/retrained_labels.txt")]

# Unpersists graph from file
with tf.gfile.FastGFile("../images/retrained_graph.gb", 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    _ = tf.import_graph_def(graph_def, name='')

islands_f = open('islands.txt', 'w')
continents_f = open('continents.txt', 'w')

with tf.Session(config=tf.ConfigProto(log_device_placement=True)) as sess:
	softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

	for image_path in os.listdir(path):
		if image_path[-3:] != 'jpg'
			continue
		# Read in the image_data
		image_data=(tf.gfile.FastGFile(path + '/' + image_path, 'rb').read())
		predictions = sess.run(softmax_tensor, \
			{'DecodeJpeg/contents:0': image_data})


		# Sort to show labels of first prediction in order of confidence
		top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
		
		t = 0
		for node_id in top_k:
			human_string = label_lines[node_id]
			score = predictions[0][node_id]
			if t%2 == 0:
				if 'island' in human_string:
					islands_f.write(image_path + '\t' + str(score) + '\n')
				else:
					continents_f.write(image_path + '\t' + str(score) + '\n')
		t += 1
islands_f.close()
continents_f.close()
