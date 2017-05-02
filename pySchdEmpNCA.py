from pyschedule import Scenario, solvers, plotters, alt
import random
import time

capName = ['A', 'B', 'C', 'D']
foName =  ['E', 'F', 'G', 'H']
n_days = 14 # number of days
days = list(range(n_days))

max_seq = 3 # max number of consecutive shifts
min_seq = 1 # min sequence without gaps
max_work = 14 # max total number of shifts
min_work = 1 # min total number of shifts
max_weekend = 1 # max number of weekend shifts

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
[   ('A',0),
    ('B',5),
    ('C',8),
    ('D',2),
    ('E',9),
    ('F',5),
    ('G',1),
    ('H',7),
    ('A',3),
    ('B',4),
    ('C',4),
    ('D',9),
    ('F',1),
    ('F',2),
    ('F',3),
    ('F',5),
    ('F',7),
    ('H',13) ]

# Create employee scheduling scenari
S = Scenario('employee_scheduling', horizon=n_days)

# Create enployees as resources indexed by namesc
employeeList = capName + foName
captains = {name: S.Resource(name) for name in capName}
fos = {name: S.Resource(name) for name in foName}

# Create shifts as tasks
shifts = {(day, i): S.Task('S_%s_%s' % (str(day), str(i)), shift_requirements[day][i]) for day in shift_requirements if day in days for i in range(len(shift_requirements[day]))}

# distribute shifts to days
for day, i in shifts:
    # Assign shift to its day
    S += shifts[day, i] >= day
    # The shifts on each day are interchangeable, so add them to the same group
    shifts[day, i].group = day
    # Weekend shifts get attribute week_end
    if day % 7 in {5, 6}:
        shifts[day, i].week_end = 1

#TODO: Need to assign one Captain & One FO
# flight1 += {AliceCap|BobCap|JohnCap, MarkFO|PaulFO|PeterFO}
# There are no restrictions, any shift can be done by any employee
for day, i in shifts:
    shifts[day, i] += alt(S.resources())
    #shifts[day, i] += captains
    #shifts[day, i] += fos

# Capacity restrictions - Captains
for name in captains:
    # Maximal number of shifts
    S += captains[name] <= max_work
    # Minimal number of shifts
    S += captains[name] >= min_work
    # Maximal number of weekend shifts using attribute week_end
    S += captains[name]['week_end'] <= max_weekend

# Capacity restrictions - FOs
for name in fos:
    # Maximal number of shifts
    S += fos[name] <= max_work
    # Minimal number of shifts
    S += fos[name] >= min_work
    # Maximal number of weekend shifts using attribute week_end
    S += fos[name]['week_end'] <= max_weekend


# Max number of consecutive shifts
for name in captains:
    for day in range(n_days):
        S += captains[name][day:day + max_seq + 1] <= max_seq

# Max number of consecutive shifts
for name in fos:
    for day in range(n_days):
        S += fos[name][day:day + max_seq + 1] <= max_seq


# Min sequence without gaps
for name in captains:
    # No increase in last periods
    S += captains[name][n_days - min_seq:].inc <= 0
    # No decrease in first periods
    S += captains[name][:min_seq].dec <= 0
    # No diff during time horizon
    for day in days[:-min_seq]:
        S += captains[name][day:day + min_seq + 1].diff <= 1

# Min sequence without gaps
for name in fos:
    # No increase in last periods
    S += fos[name][n_days - min_seq:].inc <= 0
    # No decrease in first periods
    S += fos[name][:min_seq].dec <= 0
    # No diff during time horizon
    for day in days[:-min_seq]:
        S += fos[name][day:day + min_seq + 1].diff <= 1



time_limit = 15  # time limit for each run
repeats = 5  # repeated random runs because CBC might get stuck

# Iteratively add shift requests until no solution exists
for name, day in shift_requests:
    S += captains[name][day] >= 1
    S += fos[name][day] >= 1
    for i in range(repeats):
        random_seed = random.randint(0, 10000)
        start_time = time.time()
        status = solvers.mip.solve(S, kind='CBC', time_limit=time_limit, random_seed=random_seed, msg=0)
        # Break when solution found
        if status:
            break
    print(name, day, 'compute time:', time.time() - start_time)
    # Break if all computed solution runs fail
    if not status:
        S -= captains[name][day] >= 1
        S -= fos[name][day] >= 1
        print('cant fit last shift request')

# Plot the last computed solution
#plotters.matplotlib.plot(S, fig_size=(12, 5))

# Solve and plot scenario
if solvers.mip.solve(S, kind='CBC', msg=1, random_seed=6):
    print "The solution is", S.solution()
    plotters.matplotlib.plot(S, fig_size=(12, 5))
else:
    print('no solution found')