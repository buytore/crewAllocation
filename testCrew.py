from crew1 import combineFlts, dayAvailSchdHours, dayAvailSchdBinary, employeePriorHours,futureWork
from pprint import pprint

# Create Pairings

mark = combineFlts()
print "We are in Test: "
pprint(mark)
print "The length of flt records is: ", len(mark)

# Pairing Creation is successful - see who could fly

employeeData = dayAvailSchdHours(employeePriorHours)

print "This is in test - employeeData"
pprint(employeeData)
pprint(dayAvailSchdBinary(employeeData))


#employeeData = dayAvailSchdHours(employeePriorHours)
#print dayAvailSchdBinary(employeeData)