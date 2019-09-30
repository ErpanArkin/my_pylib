from ovito.data import *

def modify(frame, input, output):
    n = input.attributes['SourceFrame']
    time = 0.3 + (n - 15) * 0.3
    output.attributes['Time'] = round(time,2)
    output.attributes['Steps'] = int((n - 15) * 15)