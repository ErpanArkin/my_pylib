from ovito.data import *

def modify(frame, data, output):
    finder = NearestNeighborFinder(4, data)
    neigh = []
    for x,y in zip(data.particle_properties['Particle Type'].array,
	                            data.particle_properties['Particle Identifier'].array):
        query = {x:y}
        if x == 3:
            neigh.append(y)
            print(y)
            for i in finder.find(y):
                neigh.append(i)
    
    print(len(neigh))
 