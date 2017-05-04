from pyschedule import Scenario, solvers, plotters, alt
import random
import time

employeeNames = {
    'Alice': 'Captain',
    'Bob': 'Captain',
    'John': 'Captain',
    'Sarah': 'Captain',
    'Mark': 'FO',
    'Paul': 'FO',
    'Peter': 'FO',
    'Jay': 'FO'
}

n_days = 14 # number of days
days = list(range(n_days))

max_seq = 5 # max number of consecutive shifts
min_seq = 2 # min sequence without gaps
max_work = 10 # max total number of shifts
min_work = 7 # min total number of shifts
max_weekend = 3 # max number of weekend shifts

# number of required shifts for each day
shift_requirements =\
{   0: [2, 6, 3],
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
    13: [3, 6] }

# specific shift requests by employees for days
shift_requests =\
[
('Alice',0),
('Bob',5),
('John',8),
('Sarah',2),
('Mark',9),
('Paul',5),
('Peter',1),
('Jay',7),
('Alice',3),
('Bob',4),
('John',4),
('Sarah',9),
('Paul',1),
('Paul',2),
('Paul',3),
('Paul',5),
('Paul',7),
('Jay',13)
]

# Create employee scheduling scenari
S = Scenario('employee_scheduling', horizon=n_days)

# Build Resources for the Tasks
crewResourcesFO = [S.Resource('%s_%s' % (person, role)) for person, role in employeeNames.iteritems() if role == "FO"]
crewResourcesCaptain = [S.Resource('%s_%s' % (person, role)) for person, role in employeeNames.iteritems() if role == "Captain"]

#shiftTasks = {'D%dS%d' % (day, nbrShift): S.Task('Day%d_Shift%d' % (day, nbrShift), shift_requirements[day][nbrShift]) for day in days for nbrShift in range(len(shift_requirements[day])) }
shiftTasks = {(day, nbrShift): S.Task('Day%d_Shift%d' % (day, nbrShift), shift_requirements[day][nbrShift]) for day in days for nbrShift in range(len(shift_requirements[day])) }

# distribute shifts to days
for day, i in shiftTasks:
    # Assign shift to its day
    S += shiftTasks[day, i] >= day
    # The shifts on each day are interchangeable, so add them to the same group
    shiftTasks[day, i].group = day
    # Weekend shifts get attribute week_end
    if day % 7 in {5, 6}:
        shiftTasks[day, i].week_end = 1

        # Add resources to Tasks
    shiftTasks[day, i] += alt(crewResourcesFO), alt(crewResourcesCaptain)


print shiftTasks

time_limit = 10  # time limit for each run
repeats = 5  # repeated random runs because CBC might get stuck



## NEED TO FIGURE THIS OUT ##
# Iteratively add shift requests until no solution exists
employees = crewResourcesCaptain + crewResourcesFO
for name, day in shift_requests:
    resourceName = name+"_"+employeeNames[name]
    S += employees[resourceName][day] >= 1
    for i in range(repeats):
        random_seed = random.randint(0, 10000)
        start_time = time.time()
        status = solvers.mip.solve(S, kind='CBC', time_limit=time_limit,
                                   random_seed=random_seed, msg=0)
        # Break when solution found
        if status:
            break
    print(name, day, 'compute time:', time.time() - start_time)
    # Break if all computed solution runs fail
    if not status:
        S -= employees[resourceName][day] >= 1
        print('cant fit last shift request')

# Plot the last computed solution
#plotters.matplotlib.plot(S, fig_size=(12, 5))

# Solve and plot scenario
if solvers.mip.solve(S, kind='CBC', msg=1, random_seed=6):
    print "The solution is", S.solution()
    plotters.matplotlib.plot(S, fig_size=(12, 5))
else:
    print('no solution found')