from crew1 import combineFlts, dayAvailSchdHours, dayAvailSchdBinary, employeePriorHours, futureFlyingHrs, dayAvailSchdDaysOff, convertDT
from pprint import pprint
from googleDateConvert import formatPairings

# Create Pairings

mark = combineFlts()
print "We are in Test: "
pprint(mark)
print "The length of flt records is: ", len(mark)

convertDT(mark)
#TODO build visualization of the pairing schedule
pairingsList = combineFlts()
cleanPairings = formatPairings(pairingsList)
pairingsDF = convertDT(pairingsList)

#print convertToPairsHrs(mark)

# Pairing Creation is successful - see who could fly based on Pairing Schd & Times

employeeData = dayAvailSchdHours(employeePriorHours)

print "This is in test - employeeData"
pprint(employeeData)

# TEST - Build a Schedule for employee
binarySchd = dayAvailSchdBinary(employeeData)
pprint(binarySchd)

pprint(dayAvailSchdDaysOff(employeeData))



