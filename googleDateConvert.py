import datetime
import time
from random import randint

def formatPairingsTimeline(pairingList):
    formatGoogleList = ""
    row_data = ""
    count = 0
    for newJSON in pairingList:
        aircraftTail = " ".join(newJSON["ac"])
        if count >= 0 and count < len(pairingList) - 1:
            row_data += '["' + aircraftTail + '", "' + aircraftTail + '", ' + \
                            'new Date(' + datetime.datetime.strptime(str(newJSON["startDate"]), '%Y-%m-%d %H:%M:%S').strftime('%Y,%m-1,%d, %H, %M, %S') + '), ' \
                            'new Date(' + datetime.datetime.strptime(str(newJSON["endDate"]), '%Y-%m-%d %H:%M:%S').strftime('%Y,%m-1,%d, %H, %M, %S') + ')'\
                            +  '], '
        else:
            row_data += '["' + aircraftTail + '", "' + aircraftTail + '", ' + \
                            'new Date(' + datetime.datetime.strptime(str(newJSON["startDate"]), '%Y-%m-%d %H:%M:%S').strftime('%Y,%m-1,%d, %H, %M, %S') + '), ' \
                            'new Date(' + datetime.datetime.strptime(str(newJSON["endDate"]), '%Y-%m-%d %H:%M:%S').strftime('%Y,%m-1,%d, %H, %M, %S') + ')'\
                            +  ']'
            count = 0
        count += 1
    formatGoogleList = '[' + row_data + ']'

    return formatGoogleList


def buildGoogleFormatBar(rawData, fetchData):
    """Takes a SQLAlchemy query result (rawData) & SQLAlchemy fetchall (fetchData)
       processes and convert to LIST
       RETURNS: Google Chart ready array"""
    headerList=[]
    dataList = []
    rowList = []

    #Build the Google tabledata array header
    for columnName in rawData._metadata.keys:        #gets table column names
        if columnName == "Colour":
            columnName = {'role': 'style'}
            headerList.append(dict(columnName))
        elif columnName == "Annotate":
            columnName = {'role': 'annotation'}
            headerList.append(dict(columnName))
        else:
            headerList.append(str(''.join(columnName)))
    dataList.append(headerList)

    for entry in fetchData:
        for column in entry:
            if isinstance(column, datetime):
                rowList.append('new Date(' + datetime.strptime(str(column), '%Y-%m-%d %H:%M:%S').strftime('%Y,%m-1,%d') + '_)')
            elif isinstance(column, int):
                rowList.append(str('int('+str(column)+')'))
            else:
                rowList.append(str(column))
        dataList.append(rowList)
        rowList=[]
    dataTableProd = str(dataList)+ ', false'

    upDataTableProd = googlePrepData(dataTableProd)
    return upDataTableProd