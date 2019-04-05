import ovito

'''
print a charge on a atom
'''

def render(painter, **args):

	node = ovito.dataset.selected_node
	Li_charge = node.source.particle_properties['Charge'].array[-1]
	painter.drawText(painter.window().width()/2-40, painter.window().height()/2 -100, 'charge on Li:'+str(Li_charge))
