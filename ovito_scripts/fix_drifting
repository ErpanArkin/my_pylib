from ovito.data import *

def modify(frame, input, output):
	print("The input contains %i particles." % input.number_of_particles)
	
	#print(input.particle_properties.keys())
	drifting_vector = input.particle_properties['Displacement'].marray.mean(axis=0)
	
	new_position = input.particle_properties['Position'].marray - drifting_vector
	print("Drifting vector: {}".format(drifting_vector))
	
	output.particle_properties['Position'].marray[:] = new_position

	output.particle_properties['Position'].changed()