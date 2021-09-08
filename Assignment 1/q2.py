class DistrictNode:
    def __init__(self, name):
        self.name = name
        self.neigh = []
    
    def addNeighbour(self, objAdd):
        self.neigh.append(objAdd)

import json

with open('out/neighbor-districts-modified.json') as ndjson:
    nds = json.load(ndjson)

allDist = list(nds.keys())
grph_map = {}
visited = {}

for dist in allDist:
    grph_map[dist] = DistrictNode(dist)
    visited[dist] = False

for dist in allDist:
    for nd in nds[dist]:
        grph_map[dist].addNeighbour(grph_map[nd])

# grph_map is the required graph

lines = []

def dfs(gNode, parents):
    visited[gNode.name] = True
    parents.append(gNode.name)
    for dObj in gNode.neigh:
        if dObj.name not in parents:
            lines.append(gNode.name+","+dObj.name+"\n")
        if not visited[dObj.name]:
            dfs(dObj, parents)
    parents.pop()

for aDist in allDist:
    if not visited[aDist]: dfs(grph_map[aDist], [])

with open("out/edge-graph.csv", "w") as edg:
    edg.writelines(lines)