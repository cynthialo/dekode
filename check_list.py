#!/usr/bin/env python
# This code will check the folder and some subfolder assigned by the user to see if the mp-*** listed in a text file are available or not
# If available, the selected property at selected concentration and temperature will be reported
# If not, N.A would be typed in front of the list
# By: Alireza Faghaninia


#!/usr/bin/env python

import argparse
import os

def find_properties(filename, n, T): #find the transport properties at a given n and T from aMoBT output
	count = 0
	mobility = 0
	conductivity = 0
	thermopower = 0
	at_correct_n = False
	if os.path.exists(filename):
		with open(filename) as aMoBT_output:
			for row in aMoBT_output:
				line = row.split()
				if at_correct_n:
					if float(line[0]) == T:
						mobility = float(line[1])
						conductivity = float(line[2])
						thermopower = float(line[3])
						at_correct_n = False
				if len(line) > 3:
					if 'Carrier' in line[0] and float(line[3]) == n:
						at_correct_n = True
	return mobility, conductivity, thermopower

def find_effective_mass(filename):
	m_e = 0.0000
	m_h = 0.0000
	if os.path.exists(filename):
		with open(filename) as aMoBT_output:
			for row in aMoBT_output:
				line = row.split()
				if len(line) >= 2:
					if line[0] == '***Proceed':
						if 'm*_e/m' in line[7]:
							m_e = float(line[9])
						if 'm*_h/m' in line[7]: 
							m_h = float(line[9])
	return m_e, m_h

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-f", "--filename", help="The filename that contains the list, default=checklist",	required=False, default="checklist")
	parser.add_argument("-n", "--n", help="Carrier concentration", required=False, default=1e21)
	parser.add_argument("-T", "--T", help="Temperature(K)", required=False, default=300)
	parser.add_argument("-d", "--free_e", help="To use free-electron density of states or not ('''true''' or '''false''')", required=False, default="true")
	args = parser.parse_args()
	folders = ['./', 'new_TEs/', 'new_TCOs/']
	n_type_folder = '1_n-type_aMoBT_free-e=' + args.free_e
	p_type_folder = '2_p-type_aMoBT_free-e=' + args.free_e
	clist = []
	with open(args.filename,'r') as raw_list:
		for line in raw_list:
			if len(line)>1:
				supposed_id = line.split()[0]
				if ('mp-' in supposed_id) or ('mvc-' in supposed_id):
					clist.append(line.split()[0])
	stat = open('status.txt', 'w')
	rem = open('remaining.txt', 'w')
	stat.write('%30s%15s%12s %10s%10s%10s%10s\n' % ('location of mp-id (if any)', 'mu-cm2/V.s', 'sigma-S/cm', 'S-uV/K', 'p_mu', 'p_sigma', 'p_S' ))
	for c in clist:
		proceed = False
		for subf in folders:
			if os.path.exists(subf + c):
				proceed = True
				c = subf + c
		if proceed:
			stat.write('%30s\n' % c)
		else:
			stat.write('%30s%15s\n' % (c, 'N.A.'))
			mpstart = c.find('mp-')
			rem.write(c[mpstart:] + '\n')
		
	stat.close()
	rem.close()
	mobility_n, conductivity_n, thermopower_n = find_properties(n_type_folder + '/aMoBT_output.txt', args.n, args.T)
	mobility_p, conductivity_p, thermopower_p = find_properties(p_type_folder + '/aMoBT_output.txt', args.n, args.T)
