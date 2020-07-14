#! /usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import sys

def usage():
	print(
"""\
USAGE: covid19.py path/to/covid-19-data [OPTIONS]... [LOCATIONS]...
LOCATIONS:
  "US" | state | county,state
OPTIONS:
  --log       : use a logarithmic y-axis (default is linear)
  --deaths    : graph number of deaths (default is number of cases)
  --diff      : graph the first derivative of cases/deaths in addition to just cases/deaths
  --diff-only : only graph the first derivative of cases/deaths

EXAMPLE:
  covid19.py path/to/covid-19-data --log --deaths --diff-only "US" "New York" "Boulder,Colorado"
    Graph the first derivative of the number of COVID deaths, on a logarithmic scale, in the US, the state of New York, and Boulder County
""")
	exit(1)

graphAx = None
doLog = False

doTotal = True
doDiff = False

selector = "cases"


def drawState(data, state):
	global graphAx
	state_only = (data.loc[data['state'] == state])[['date', selector]]
	state_only['date'] = pd.to_datetime(state_only['date'], format="%Y-%m-%d")
	state_only = state_only.set_index('date')
	state_diff = state_only.diff()
	state_only = state_only.rename(columns={selector: f'{state}'})
	state_diff = state_diff.rename(columns={selector: f'(d/dt) {state}'})
	
	if doTotal:
		graphAx = state_only.plot(ax = graphAx, logy = doLog)
	if doDiff:
		graphAx = state_diff.plot(ax = graphAx, logy=doLog)

def drawCounty(data, state, county):
	global graphAx
	county_only = ((data.loc[data['state'] == state]).loc[data['county'] == county])[['date', selector]]
	county_only['date'] = pd.to_datetime(county_only['date'], format="%Y-%m-%d")
	county_only = county_only.set_index('date')
	county_diff = county_only.diff()
	county_only = county_only.rename(columns={selector: f'{county}, {state}'})
	county_diff = county_diff.rename(columns={selector: f'(d/dt) {county}, {state}'})
	
	if doTotal:
		graphAx = county_only.plot(ax = graphAx, logy = doLog)
	if doDiff:
		graphAx = county_diff.plot(ax = graphAx, logy = doLog)

def drawUS(data):
	global graphAx
	data = data[['date', selector]]
	data = data.groupby('date')[selector].sum().reset_index()
	data['date'] = pd.to_datetime(data['date'], format="%Y-%m-%d")
	data = data.set_index('date')
	diff = data.diff()
	data = data.rename(columns={selector: 'United States'})
	diff = diff.rename(columns={selector: '(d/dt) United States'})

	if doTotal:
		graphAx = data.plot(ax = graphAx, logy = doLog)
	if doDiff:
		graphAx = diff.plot(ax = graphAx, logy = doLog)

def main():
	global doLog, doDiff, doTotal, selector
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
			elif area[0] == '--deaths':
				selector = "deaths"
			elif area[0] == '--diff-only':
				doTotal = False
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

		
	plt.grid()
	plt.show()

main()
