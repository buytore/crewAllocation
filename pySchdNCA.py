from pyschedule import Scenario, solvers, plotters

#setup scenario - limit length of day to 15 (15 hours duty day)
S = Scenario('NCA_Crew_Schd', horizon=15)

AliceCap = S.Resource('AliceCap')
BobCap = S.Resource('BobCap')
JohnCap = S.Resource('JohnCap')
MarkFO = S.Resource('MarkFO')
PaulFO = S.Resource('PaulFO')
PeterFO = S.Resource('PeterFO')

#Setup and create each job or task
# OPTION TODO: add preflight Duty, flight and then post flight
flight1 = S.Task('flight1', length=2.5)
flight2 = S.Task('flight2', length=4)
flight3 = S.Task('flight3', length=6)


#Add Constraints
S += flight1 < flight2, flight3 + 1 <= flight2
S += AliceCap['length'] <= 3
S += JohnCap['length'] <= 4
S += BobCap['length'] <= 6


# Assign tasks/jobs - below indicates that any resource can do the job
flight1 += {AliceCap|BobCap|JohnCap, MarkFO|PaulFO|PeterFO}
flight2 += {AliceCap|BobCap|JohnCap, MarkFO|PaulFO|PeterFO}
flight3 += {AliceCap|BobCap|JohnCap, MarkFO|PaulFO|PeterFO}


S.clear_solution()
S.use_makespan_objective()
print(S)

# Set some colors for the tasks
task_colors = { flight1   : '#A1D372',
                flight2    : '#A1D372',
                flight3     : '#EB4845',
                S['MakeSpan'] : '#7EA7D8'}

# A small helper method to solve and plot a scenario
def run(S) :
    if solvers.mip.solve(S):
        plotters.matplotlib.plot(S,task_colors=task_colors,fig_size=(10,5))
    else:
        print('no solution exists')

run(S)