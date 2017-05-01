from pyschedule import Scenario, solvers, plotters, alt
import random
import time

capName = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
#foName =  ['E', 'F', 'G', 'H']
n_days = 14 # number of days
days = list(range(n_days))

max_seq = 3 # max number of consecutive shifts
min_seq = 1 # min sequence without gaps
max_work = 14 # max total number of shifts
min_work = 1 # min total number of shifts
max_weekend = 1 # max number of weekend shifts

# number of required shifts for each day
shift_requirements =\
{   0: 3,
    1: 1,
    2: 2,
    3: 3,
    4: 2,
    5: 1,
    6: 2,
    7: 2,
    8: 2,
    9: 1,
    10: 2,
    11: 3,
    12: 2,
    13: 2 }

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
employeeList = capName
employees = {name: S.Resource(name) for name in employeeList}

# Create shifts as tasks
shifts = {(day, i): S.Task('S_%s_%s' % (str(day), str(i)),5)
          for day in shift_requirements if day in days
          for i in range(shift_requirements[day])}

# distribute shifts to days
for day, i in shifts:
    # Assign shift to its day
    S += shifts[day, i] >= day
    # The shifts on each day are interchangeable, so add them to the same group
    shifts[day, i].group = day
    # Weekend shifts get attribute week_end
    if day % 7 in {5, 6}:
        shifts[day, i].week_end = 1

# There are no restrictions, any shift can be done by any employee
for day, i in shifts:
    shifts[day, i] += alt(S.resources())


# Capacity restrictions
for name in employees:
    # Maximal number of shifts
    S += employees[name] <= max_work
    # Minimal number of shifts
    S += employees[name] >= min_work
    # Maximal number of weekend shifts using attribute week_end
    S += employees[name]['week_end'] <= max_weekend

# Max number of consecutive shifts
for name in employees:
    for day in range(n_days):
        S += employees[name][day:day + max_seq + 1] <= max_seq

# Min sequence without gaps
for name in employees:
    # No increase in last periods
    S += employees[name][n_days - min_seq:].inc <= 0
    # No decrease in first periods
    S += employees[name][:min_seq].dec <= 0
    # No diff during time horizon
    for day in days[:-min_seq]:
        S += employees[name][day:day + min_seq + 1].diff <= 1


time_limit = 15  # time limit for each run
repeats = 5  # repeated random runs because CBC might get stuck

# Iteratively add shift requests until no solution exists
for name, day in shift_requests:
    S += employees[name][day] >= 1
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
        S -= employees[name][day] >= 1
        print('cant fit last shift request')

# Plot the last computed solution
#plotters.matplotlib.plot(S, fig_size=(12, 5))

# Solve and plot scenario
if solvers.mip.solve(S, kind='CBC', msg=1, random_seed=6):
    print "The solution is", S.solution()
    plotters.matplotlib.plot(S, fig_size=(12, 5))
else:
    print('no solution found')