import os
import re

simple = {}  # Dictionary of underlying graphs

def load_graphs(f_name, lst):
	with open(f_name, 'r') as f_in:
		for line in f_in:
			g6s = line.strip()
			if g6s:
				lst.append(g6s)

# Load all data
file_name_pattern = r'underlying\_(\d+)\.g6'

for f_name in os.listdir('.'):
	m = re.match(file_name_pattern, f_name)
	if m is not None:
		number_of_orbits = int(m.group(1))
		simple[number_of_orbits] = []
		load_graphs(f_name, simple[number_of_orbits])

# $ ./geng -c -D3 4
# simple[4] = ['CF', 'CU', 'CV', 'C]', 'C^', 'C~'] 
 
# $ ./geng -c -D3 5
# simple[5] = [
#     'DCw', 'DEw', 'DEk', 'DFw', 'DQo', 'DQw', 'DUW', 'DUw', 'DTw', 'D]w'
# ]
