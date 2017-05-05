from pyschedule import Scenario, solvers, plotters, alt
import random
import time

n_days = 14 # number of days
days = list(range(n_days))
max_seq = 10 # max number of consecutive shifts
min_seq = 2 # min sequence without gaps
max_work = 28 # max total number of shifts
min_work = 2 # min total number of shifts
max_weekend = 3 # max number of weekend shifts

employeeNames = {
                    'Alice':    'Captain',
                    'Bob':      'Captain',
                    'John':     'Captain',
                    'Sarah':    'Captain',
                    'Mark':     'FO',
                    'Paul':     'FO',
                    'Peter':    'FO',
                    'Jay':      'FO'
                }

# number of required shifts for each day
# list contain each flight and the respective flight time
shift_requirements ={   0: [2, 6, 3],
                        1: [5],
                        2: [2, 4],
                        3: [3, 3, 5],
                        4: [4, 3],
                        5: [7],
                        6: [3, 6],
                        7: [4, 6],
                        8: [6, 5],
                        9: [6],
                        10: [2, 4],
                        11: [5, 3, 6],
                        12: [6, 5],
                        13: [3, 6]
                    }

# Create employee scheduling scenari
S = Scenario('employee_scheduling', horizon=n_days)

# Build Resources for the Tasks
crewResourcesFO = [S.Resource('%s_%s' % (person, role)) for person, role in employeeNames.iteritems() if role == "FO"]
crewResourcesCaptain = [S.Resource('%s_%s' % (person, role)) for person, role in employeeNames.iteritems() if role == "Captain"]

#Build Shifts within Days as Tasks
shiftTasks = {(day, nbrShift): S.Task('Day%d_Shift%d' % (day, nbrShift), shift_requirements[day][nbrShift]) for day in days for nbrShift in range(len(shift_requirements[day])) }

# distribute shifts to days
for day, i in shiftTasks:
    # Assign shift to its day
    S += shiftTasks[day, i] >= day
    # The shifts on each day are interchangeable, so add them to the same group
    shiftTasks[day, i].group = day

    # Add resources to Tasks - TODO: should look at a way to eliminate "unavailable crew members" at this point.
    shiftTasks[day, i] += alt(crewResourcesFO), alt(crewResourcesCaptain)

print shiftTasks

employees = crewResourcesCaptain + crewResourcesFO
# Capacity restrictions
for name in employees:
    # Maximal number of shifts
    S += name <= max_work
    # Minimal number of shifts
    S += name >= min_work

# Max number of consecutive shifts
for name in employees:
    for day in range(n_days):
        S += name[day:day + max_seq + 1] <= max_seq

# Min sequence without gaps
for name in employees:
    # No increase in last periods
    S += name[n_days - min_seq:].inc <= 0
    # No decrease in first periods
    S += name[:min_seq].dec <= 0
    # No diff during time horizon
    for day in days[:-min_seq]:
        S += name[day:day + min_seq + 1].diff <= 1

# Solve and plot scenario
if solvers.mip.solve(S, kind='CBC', msg=1, random_seed=6):
    print "The solution is", S.solution()
    plotters.matplotlib.plot(S, fig_size=(12, 5))
else:
    print('no solution found')