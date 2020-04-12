#! /usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import sys

def usage():
	print("Usage: covid19.py path/to/covid-19-data [options]... [area]...\narea: \"US\" | state | county,state\noptions:\n\t--log\t:logarithmic y axis\n\t--diff\t:plot 1st derivatives of cases")
	exit(1)

graphAx = None
doLog = False
doDiff = False

def drawState(data, state):
	global graphAx
	state_only = (data.loc[data['state'] == state])[['date', 'cases']]
	state_only['date'] = pd.to_datetime(state_only['date'], format="%Y-%m-%d")
	state_only = state_only.set_index('date')
	state_diff = state_only.diff()
	state_only = state_only.rename(columns={'cases': f'{state}'})
	state_diff = state_diff.rename(columns={'cases': f'(d/dt) {state}'})
	
	if graphAx == None:
		graphAx = state_only.plot(logy = doLog)
	else:
		state_only.plot(ax = graphAx, logy = doLog)
	
	if doDiff:
		state_diff.plot(ax = graphAx, logy=doLog)

def drawCounty(data, state, county):
	global graphAx
	county_only = ((data.loc[data['state'] == state]).loc[data['county'] == county])[['date', 'cases']]
	county_only['date'] = pd.to_datetime(county_only['date'], format="%Y-%m-%d")
	county_only = county_only.set_index('date')
	county_diff = county_only.diff()
	county_only = county_only.rename(columns={'cases': f'{county}, {state}'})
	county_diff = county_diff.rename(columns={'cases': f'(d/dt) {county}, {state}'})
	
	if graphAx == None:
		graphAx = county_only.plot(logy = doLog)
	else:
		county_only.plot(ax = graphAx, logy = doLog)
	
	if doDiff:
		county_diff.plot(ax = graphAx, logy = doLog)

def drawUS(data):
	global graphAx
	data = data[['date', 'cases']]
	data = data.groupby('date')['cases'].sum().reset_index()
	data['date'] = pd.to_datetime(data['date'], format="%Y-%m-%d")
	data = data.set_index('date')
	diff = data.diff()
	data = data.rename(columns={'cases': 'United States'})
	diff = diff.rename(columns={'cases': '(d/dt) United States'})

	if graphAx == None:
		graphAx = data.plot(logy = doLog)
	else:
		data.plot(ax = graphAx, logy = doLog)
	
	if doDiff:
		diff.plot(ax = graphAx, logy = doLog)

def main():
	global doLog, doDiff
	if(len(sys.argv) < 2):
		usage()
	state_file = sys.argv[1] + "/us-states.csv"
	state_data = pd.read_csv(state_file)
	county_file = sys.argv[1] + "/us-counties.csv"
	county_data = pd.read_csv(county_file)
	for i in range(2, len(sys.argv)):
		area = sys.argv[i].split(',')
		if area[0][0:2] == '--':
			if area[0] == '--log':
				doLog = True
			elif area[0] == '--diff':
				doDiff = True
			else:
				usage()
		elif area[0] == 'US':
			drawUS(state_data)
		elif len(area) == 1:
			drawState(state_data, area[0])
		elif len(area) == 2:
			drawCounty(county_data, area[1], area[0])
		else:
			usage()
	
	plt.show()

main()
