from ovito.data import *
import numpy

def modify(frame, input, output):
	print("The input contains %i particles." % input.number_of_particles)
	cluster_types = numpy.bincount(input.particle_properties['Cluster'].array)
	x = {}
	for i,j in zip (input.particle_properties['Particle Type'].array,
	                input.particle_properties['Cluster'].array):
		if j not in x.keys():
			x[j] = ''
		x[j] += str(i)
	atom_type = input.particle_properties['Particle Type'].array
	cluster_types = []
	for k in x:
		m = ''.join([str(x[k].count(j))+atom_type[j] for j in set(x[k])])
		cluster_types.append(m)
	print(cluster_types)
	print(input.particle_properties['Particle Type'].array)
	print(set(cluster_types))
	each_cluster_number = list(numpy.bincount(cluster_types))
	print(each_cluster_number)
	print("type:number")
	
