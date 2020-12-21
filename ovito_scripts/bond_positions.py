from ovito.data import *
import numpy as np

def modify(frame, data):
    
    # This user-defined modifier function gets automatically called by OVITO whenever the data pipeline is newly computed.
    # It receives two arguments from the pipeline system:
    # 
    #    frame - The current animation frame number at which the pipeline is being evaluated.
    #    data   - The DataCollection passed in from the pipeline system. 
    #                The function may modify the data stored in this DataCollection as needed.
    # 
    # What follows is an example code snippet doing nothing except printing the current 
    # list of particle properties to the log window. Use it as a starting point for developing 
    # your own data modification or analysis functions. 
    
    if data.particles != None:
        #print("There are %i particles with the following properties:" % data.particles.count)
        #for property_name in data.particles.keys():
        #    print("  '%s'" % property_name)
        #print("There are %i bonds with the following properties:" % data.bonds.count)
        #for property_name in data.bonds.keys():
        #    print("  '%s'" % property_name)
        print('# atom_type x y z bond_length')
        for i in range(data.bonds.count):
            pos = data.particles['Position'][data.bonds['Topology'][i]].copy()
            large_pos = ~(pos < np.linalg.norm(data.cell.matrix[0:3,0:3], axis=1)).all(axis=1)
            if large_pos.any():
                pos[large_pos] -= abs(np.linalg.norm(data.cell.matrix[0:3,0:3], axis=1) * data.bonds['Periodic Image'][i])
                pos_len = data.bonds['bond_length'][i]
            print('C',np.array2string(np.mean(pos,axis=0))[1:-1], pos_len)
