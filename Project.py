from pulp import *
import numpy as np
import networkx as nx

#Extracting Data File
with open("data/small_test.txt") as file:
    data = [line.rstrip() for line in file]

streets=[]
intersections=[]
for line in data:
    l = line.split()
    streets.append((int(l[0]),int(l[1]),float(l[2])))
    streets.append((int(l[1]),int(l[0]),float(l[2])))
    intersections.append(int(l[0]))
    intersections.append(int(l[1]))
intersections=list(np.unique(intersections))
print("The network has", len(streets), "streets and", len(intersections), "intersections")

#Create Model
model = LpProblem("Shortest_Path", LpMinimize)

#Define decision variables
xindx = []
for street in streets:
    xindx.append((street[0],street[1]))

x = LpVariable.dicts("X", xindx, 0, None)
model+=lpSum([street[2]*x[street[0],street[1]] for street in streets])

#Set up flow
source=0
terminal=9
for i in intersections:
    if i==source:
        model+=lpSum([x[street[0],street[1]]-x[street[1],street[0]] for street in streets if street[0]==i])==1, "source"
    elif i==terminal:
        model+=lpSum([x[street[0],street[1]]-x[street[1],street[0]] for street in streets if street[0]==i])==-1, "destination"
    else:
        model+=lpSum([x[street[0],street[1]]-x[street[1],street[0]] for street in streets if street[0]==i])==0, "node"+str(i)

model.solve()
print('Status:',LpStatus[model.status])

#Solution
for v in model.variables():
    if v.varValue==1:
        print(v.name, '=', v.varValue)
print('The travel time is',value(model.objective))
