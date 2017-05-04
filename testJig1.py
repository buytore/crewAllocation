from pyschedule import Scenario, solvers, plotters, alt
import random
import time

employee_names = ['A','B','C','D','E','F','G','H']
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
('A',0),
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
('H',13)
]

# Create employee scheduling scenari
S = Scenario('employee_scheduling', horizon=n_days)

AliceC = S.Resource('AliceCap')
BobC = S.Resource('BobCap')
JohnC = S.Resource('JohnCap')
MarkF = S.Resource('MarkFO')
PaulF = S.Resource('PaulFO')
PeterF = S.Resource('PeterFO')

#crewResources = {'%s_%s' % (person, role): S.Resource('%s_%s' % (person, role)) for person, role in employeeNames.iteritems() }
crewResourcesFO = [S.Resource('%s_%s' % (person, role)) for person, role in employeeNames.iteritems() if role == "FO"]
crewResourcesCaptain = [S.Resource('%s_%s' % (person, role)) for person, role in employeeNames.iteritems() if role == "Captain"]

shiftTasks = {'D%dS%d' % (day, nbrShift): S.Task('Day%d_Shift%d' % (day, nbrShift), shift_requirements[day][nbrShift]) for day in days for nbrShift in range(len(shift_requirements[day])) }

for day in days:
    for nbrShift in range(len(shift_requirements[day])):
        key = 'D%dS%d' % (day, nbrShift)
        #shiftTasks[key] += {AliceC|BobC|JohnC, MarkF|PaulF|PeterF}
        shiftTasks[key] += alt(crewResourcesFO), alt(crewResourcesCaptain)


print shiftTasks
"""
for day in shift_requirements:
    print "Day is:", day
    for i in range(shift_requirements[day]):
        print "This is i", i
"""