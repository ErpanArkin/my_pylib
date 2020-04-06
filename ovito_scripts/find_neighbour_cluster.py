from ovito.data import *
from ovito.modifiers import *
import numpy as np

def modify(frame, data):
    finder = NearestNeighborFinder(4, data)
    query = {x:y for x,y in zip(data.particles['Particle Identifier'],data.particles['Particle Type'])}
    subset = [x == 3 for x in data.particles['Particle Type']]
    print(sum(subset))
    data_output = []
    selection = data.particles_.create_property('Selection')
    with selection:
        for index in data.particles['Particle Identifier'][subset]:
            #neigh_list = [index]
            neigh_list = []
            neigh_type = []
            #selection[index] = 1
            for neigh in finder.find(index):
                neigh_type.append(query[neigh.index+1])
                neigh_list.append(neigh.index)
            neigh_type.sort()
            #if len(np.unique(neigh_type)) == 1:
                #print(neigh_list, neigh_type)
                #for i in neigh_list:
                    #selection[i] = 1 
            data_output.append(neigh_type)
            
        cluster, counts = np.unique(data_output,return_counts=True, axis=0)    
        output = np.column_stack((cluster,counts))
        np.savetxt('4-neighbours'+str(frame)+'.txt',output)
        print(output)