from ovito.data import *

def modify(frame, input, output):
	ptype = input['Particle Type']
	elm = {ptype.get_type_by_id(i).name:0.0 for i in set(input['Particle Type'].array)}
	for i,j in zip(input['Particle Type'].array,input['Charge'].array):
		elm[ptype.get_type_by_id(i).name] += round(float(j),3)
	elm_round = {i : round(elm[i],3) for i in elm}
	elm_str = 'Charges: '
	for i,j in elm_round.items():
		elm_str += i+':'+str(j)+'e   \n'
	output.attributes['list_charge'] = elm_str
	print(elm_str)