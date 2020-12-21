from ovito.data import *
from collections import Counter
import numpy

def modify(frame, input, output):
	particle_cluster_id = input.particle_properties['Cluster'].array
	
	# get the counts of each cluster 
	cluster_types = numpy.bincount(particle_cluster_id)
	print("size:counts \n", Counter(cluster_types))
	
	# assign the size of the cluster to its composing particles
	cluster_id_size_dict = Counter(particle_cluster_id)
	particle_cluster_size = list(map(cluster_id_size_dict.get,particle_cluster_id))
	output.create_user_particle_property('Cluster_sizes', data_type = 'int', data = particle_cluster_size)
	
