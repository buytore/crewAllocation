from pyschedule import Scenario, solvers, plotters

#setup scenario - limit length of day to 15 (15 hours duty day)
S = Scenario('NCA_Crew_Schd', horizon=168)

AliceCap = S.Resource('AliceCap')
BobCap = S.Resource('BobCap')
JohnCap = S.Resource('JohnCap')
MarkFO = S.Resource('MarkFO')
PaulFO = S.Resource('PaulFO')
PeterFO = S.Resource('PeterFO')
SingleDay = S.Resource('Single_Day')
#Paint_Shop = S.Resource('Paint_Shop')

#Setup and create each job or task
# OPTION TODO: add preflight Duty, flight and then post flight
flight1 = S.Task('flight1', length=2)
flight2 = S.Task('flight2', length=4)
flight3 = S.Task('flight3', length=6)
Day1 = S.Task('Day1', length=24)
Day2 = S.Task('Day2', length=24)
Day3 = S.Task('Day3', length=24)
Day4 = S.Task('Day4', length=24)
Day5 = S.Task('Day5', length=24)
Day6 = S.Task('Day6', length=24)
Day7 = S.Task('Day7', length=24)


#Add Constraints
S += flight1 < flight2, flight3 + 1 <= flight2
S += AliceCap['length'] <= 3
S += JohnCap['length'] <= 4
S += BobCap['length'] <= 6
S += Day1 < Day2, Day2 < Day3, Day3 < Day4, Day4 < Day5, Day5 < Day6, Day6 < Day7


# Assign tasks/jobs - below indicates that any resource can do the job
flight1 += {AliceCap|BobCap|JohnCap, MarkFO|PaulFO|PeterFO}
flight2 += {AliceCap|BobCap|JohnCap, MarkFO|PaulFO|PeterFO}
flight3 += {AliceCap|BobCap|JohnCap, MarkFO|PaulFO|PeterFO}


Day1 += SingleDay
Day2 += SingleDay
Day3 += SingleDay
Day4 += SingleDay
Day5 += SingleDay
Day6 += SingleDay
Day7 += SingleDay

flight1 += SingleDay

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