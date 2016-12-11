from collections import defaultdict
from datetime import datetime

employeePriorHours = {'Mark': [6, 4, 7, 3, 4, 9, 5, 7, 8, 6, 9 , 7],
                    'Irina': [8, 4, 2, 3, 7, 9, 5, 7, 6, 6, 5, 4],
                    'Bijan': [3, 6, 9, 3, 6, 9, 5, 7, 8, 6, 9, 7]}

# Output =  one month < 10 total hours
#           three months < 25 total hours
#           6 months < 50 total hours
#           12 months < 75 total hours
keys = ['one', 'three', 'six','twelve']

#Days to look ahead in the schedule for flights
days = range(1,13,1)
#Regulatory Flight Max - should probably be tuple (13.0, 704), (13.25, 705) with CARs standard (705, 704, 703, etc)
maxAirTime = 13.00
maxDutyTimeStartDec = 0.5
maxDutyTimeEndDec = 0.25
maxDutyTimeStartHrs = datetime.strptime('00:30', "%H:%M")
maxDutyTimeEndHrs = datetime.strptime('00:15', "%H:%M")

#Simple hours per day of flying for testing
futureWork = [3, 0, 8, 8, 7, 0, 5, 8, 7, 0, 5, 4]

# Expected or Likely format from flight schedule - SQL call
futureFlightSchd =[{'ac': 'ABC', 'day': 1, 'start': '08 Dec 2016 10:00', 'end': '08 Dec 2016 16:15'}, \
                   {'ac': 'EFG', 'day': 1, 'start': '08 Dec 2016 10:00', 'end': '08 Dec 2016 16:00'}, \
                   {'ac': 'XYZ', 'day': 1, 'start': '08 Dec 2016 10:00', 'end': '08 Dec 2016 16:00'},\
                   {'ac': 'ABC', 'day': 3, 'start': '10 Dec 2016 08:00', 'end': '10 Dec 2016 12:35'}, \
                   {'ac': 'EFG', 'day': 3, 'start': '10 Dec 2016 14:00', 'end': '10 Dec 2016 16:00'},\
                   {'ac': 'XYZ', 'day': 3, 'start': '10 Dec 2016 10:00', 'end': '10 Dec 2016 16:00'}, \
                   {'ac': 'ABC', 'day': 4, 'start': '11 Dec 2016 10:00', 'end': '11 Dec 2016 16:15'}, \
                   {'ac': 'EFG', 'day': 4, 'start': '11 Dec 2016 10:00', 'end': '11 Dec 2016 16:00'}, \
                   {'ac': 'XYZ', 'day': 4, 'start': '11 Dec 2016 10:00', 'end': '11 Dec 2016 16:00'}, \
                   {'ac': 'ABC', 'day': 5, 'start': '12 Dec 2016 08:00', 'end': '12 Dec 2016 12:35'}, \
                   {'ac': 'EFG', 'day': 5, 'start': '12 Dec 2016 14:00', 'end': '12 Dec 2016 16:00'}, \
                   {'ac': 'XYZ', 'day': 5, 'start': '12 Dec 2016 10:00', 'end': '12 Dec 2016 16:00'}, \
                   {'ac': 'ABC', 'day': 7, 'start': '14 Dec 2016 10:00', 'end': '14 Dec 2016 13:15'}, \
                   {'ac': 'STU', 'day': 7, 'start': '14 Dec 2016 15:00', 'end': '14 Dec 2016 18:25'}, \
                   {'ac': 'XYZ', 'day': 7, 'start': '14 Dec 2016 10:00', 'end': '14 Dec 2016 16:00'}]

def futFliteSchdDec():
    futFltSchdDec = {}
    futFltSchdDecList = []
    for fltRec in futureFlightSchd:
        fltTimeStart =  datetime.strptime(fltRec['start'], "%d %b %Y %H:%M")
        fltTimeEnd = datetime.strptime(fltRec['end'], "%d %b %Y %H:%M")
        totFltTime = float((fltTimeEnd - fltTimeStart).seconds / 3600.0)
        futFltSchdDec['ac'] = fltRec['ac']
        futFltSchdDec['day'] = fltRec['day']
        futFltSchdDec['totTime'] = totFltTime
        futFltSchdDecList.append(futFltSchdDec)
        print futFltSchdDec
        futFltSchdDec = {}
    return futFltSchdDecList


def combineFlts():
    """Checks to ensure flight(s) do not exceed 13 hrs (Air Time - Duty)
        Also checks if flight on same or different aircraft have 60 minute in between (can be operated by same crew)
        OUTPUT: List of Dicts
                [{'ac': ['abc', 'efg'], 'day': 1, 'startTime': 08:00, 'endTime': 16:15, totalTime: 8.25, valid: 1},
                 {'ac': ['xyz'], 'day': 1, 'startTime': 10:00, 'endTime': 16:30, totalTime: 6.30, valid: 1}"""
    futFltSchdDec = {}
    futFltSchdDecList = []
    aircraftList = []
    def buildValidFltSchd(flag = True):
        futFltSchdDec['ac'] = fltRec['ac']
        futFltSchdDec['day'] = fltRec['day']
        futFltSchdDec['totTime'] = totFltTime
        futFltSchdDecList.append(futFltSchdDec)

    lastDayValue = None
    lastEndTimeValue = None
    newFltTotTime = 0.0
    counter = 0
    for fltRec in futureFlightSchd:
        #Check for enough time between flights
        fltTimeStart = datetime.strptime(fltRec['start'], "%d %b %Y %H:%M")
        fltTimeEnd = datetime.strptime(fltRec['end'], "%d %b %Y %H:%M")
        totFltTime = float((fltTimeEnd - fltTimeStart).seconds / 3600.0)
        #Try to build separate flights into singles
        if fltRec['day'] == lastDayValue and lastEndTimeValue < fltTimeStart:
            # Add flt to prior days flt - Build ac list, store startTime
            newFltTotTime += totFltTime
            if newFltTotTime < maxAirTime:
                #UPDATE RECORD AND SECOND FLIGHTS DATA.
                futFltSchdDecList[-1]['ac'].append(fltRec['ac'])
                futFltSchdDecList[-1]['endDate'] = fltTimeEnd
                futFltSchdDecList[-1]['totTime'] = newFltTotTime
            else:
                newFltTotTime = totFltTime
                lastDayValue = fltRec['day']
                lastEndTimeValue = datetime.strptime(fltRec['end'], "%d %b %Y %H:%M")
                tempDict = fltRec
                futFltSchdDec['ac'] = [fltRec['ac']]
                futFltSchdDec['day'] = fltRec['day']
                futFltSchdDec['startDate'] = fltTimeStart
                futFltSchdDec['endDate'] = fltTimeEnd
                futFltSchdDec['totTime'] = newFltTotTime
                futFltSchdDec['valid'] = 1
                futFltSchdDecList.append(futFltSchdDec)
                futFltSchdDec = {}
        else:
            #write the record out to new List of Dicts
            newFltTotTime = totFltTime
            lastDayValue = fltRec['day']
            lastEndTimeValue = datetime.strptime(fltRec['end'], "%d %b %Y %H:%M")
            tempDict = fltRec
            futFltSchdDec['ac'] = [fltRec['ac']]
            futFltSchdDec['day'] = fltRec['day']
            futFltSchdDec['startDate'] = fltTimeStart
            futFltSchdDec['endDate'] = fltTimeEnd
            futFltSchdDec['totTime'] = newFltTotTime
            futFltSchdDec['valid'] = 1
            futFltSchdDecList.append(futFltSchdDec)
            futFltSchdDec = {}
        counter += 1
    return futFltSchdDecList

mark = combineFlts()
print mark, len(mark)
print futFliteSchdDec()

def readEmpData(empHistInfo = employeePriorHours, factor=True):
    oneMonth = 0
    threeMonths = 0
    sixMonths = 0
    twelveMonths = 0
    if factor == False:
        factorRate = 0.8
    else:
        factorRate = 1.0
    maxOneMonth = 10 * factorRate
    maxThreeMonths = 25 * factorRate
    maxSixMonths = 50 * factorRate
    maxTwelveMonths = 75 * factorRate

    empData = {}

    for employee in empHistInfo.iteritems():
        empData[employee[0]] = {}
        tally = 0
        counter = 1
        #GET EMPLOYEE NAME and build DICT
        for month in employee[1]:
            tally += month
            if counter == 1:
                oneMonth = tally
                if oneMonth < maxOneMonth:
                    empData[employee[0]][keys[0]] = oneMonth
                else:
                    del empData[employee[0]]
                    break
            elif counter == 3:
                threeMonths = tally
                if threeMonths < maxThreeMonths:
                    empData[employee[0]][keys[1]] = threeMonths
                else:
                    del empData[employee[0]]
                    break
            elif counter == 6:
                sixMonths = tally
                if sixMonths < maxSixMonths:
                    empData[employee[0]][keys[2]] = sixMonths
                else:
                    del empData[employee[0]]
                break
            elif counter == 12:
                twelveMonths = tally
                if twelveMonths < maxTwelveMonths:
                    empData[employee[0]][keys[3]] = twelveMonths
                else:
                    del empData[employee[0]]
                    break
            counter += 1
    return empData


# PROBABLY NOT NECESSARY - BUT JUST IN CASE THE SQL REQUIRES
# Make a list of employees and there associated prior hours of work - no Summing
def readEmpTime():
    empData = {}
    for employee in employeePriorHours.iteritems():
        hourList = []
        empData[employee[0]] = {}
        # GET EMPLOYEE NAME and build DICT
        for month in employee[1]:
            hourList.append(month)
        empData[employee[0]] = hourList
    return empData


def dayAvailSchdHours(empHistInfo = employeePriorHours):
    compFuture = {}
    schdFutureList = []
    for employee in empHistInfo.iteritems():
        empFuture = {}
        histTime = employee[1]
        histTime.extend(futureWork)
        for day in days:
            tally = 0
            histTimeA = histTime[1:13]
            histTimeA.reverse()
            count = 1
            #futSchd = []
            empFuture[employee[0]]=histTimeA
            mark = readEmpData(empFuture)  #Validate the hours
            if bool(mark):
                schdFutureList.append(mark)
                keyStr = str(day) + ''.join(mark.keys())
                compFuture[keyStr]= schdFutureList
            histTime.pop(0)
            schdFutureList = []
    mark = {}
    schdFutureList = []
    return compFuture


def dayAvailSchdBinary(compFuture):
    """Takes a dict of list
    key is employee name
    record is Employee name & CARs hours"""
    personAvailDutySchd = defaultdict(list)
    for key, record in compFuture.iteritems():
        day = int(''.join(x for x in key if x.isdigit()))
        name = ''.join(x for x in key if not x.isdigit())
        personAvailDutySchd[name].append(day)

    sortedSchd = []
    personAvailDutySchdBinary = defaultdict(list)
    for name, schd in personAvailDutySchd.iteritems():
        for i in days:
            if i in schd:
                personAvailDutySchdBinary[name].append(1)
            else:
                personAvailDutySchdBinary[name].append(0)
    return personAvailDutySchdBinary


employeeData = dayAvailSchdHours(employeePriorHours)
print dayAvailSchdBinary(employeeData)