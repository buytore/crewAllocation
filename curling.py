from pyschedule import Scenario, solvers, plotters, alt
from collections import OrderedDict
import math

nbrTeams = 16
totalNbrGames = nbrTeams - 1
nbrSheets = 4
nbrRounds = 4

rounds = {0: 4, 1: 4, 2: 4, 3: 2, 4: 1}

# Create scenario
S = Scenario('sport_scheduling', horizon=nbrRounds)

# Game tasks
Games = {i: S.Task('Game_%i'%(i)) for i in range(nbrTeams-1)}

# Team and field resources
Teams = [S.Resource('Team_%i'%i) for i in range(nbrTeams)]
Ice = [S.Resource('Ice_%i'%i) for i in range(nbrSheets)]

# Resource requirements
#for i in Games :
for i in OrderedDict(sorted(Games.items(), key=lambda t: t[0])) :
    Games[i] += [Teams[i]]
    Games[i] += alt(Ice)

# Setup constraint for games & draws to be in correct order
drawStart = 0
drawEnd = nbrTeams / 2
nbrGames = totalNbrGames
nbrDraws = nbrTeams / nbrSheets

while drawStart < nbrTeams:
    for i in range(drawStart, drawEnd):
        for j in range(drawEnd, nbrGames):
            S += Games[i] < Games[j]
    nbrDraws = int(round((drawEnd - drawStart + 1)/2,0))
    drawStart = drawEnd
    drawEnd = drawEnd + nbrDraws

S.use_makespan_objective()
if solvers.mip.solve(S,msg=1):
    plotters.matplotlib.plot(S,hide_resources=Teams,fig_size=(12,5))
else:
    print('no solution found')