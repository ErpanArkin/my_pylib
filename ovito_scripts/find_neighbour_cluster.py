from ovito.data import *

def modify(frame, data):
    finder = NearestNeighborFinder(4, data)
    query = {x:y for x,y in zip(data.particles['Particle Type'],data.particles['Particle Identifier'])}
    subset = [x == 3 for x in data.particles['Particle Type']]
    for index in data.particles['Particle Identifier'][subset]:
        neigh_list = [index]
        for neigh in finder.find(index):
            neigh_list.append(neigh.index)
        print(neigh_list)
            