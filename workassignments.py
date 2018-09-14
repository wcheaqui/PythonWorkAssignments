# Get the Date from the User
year = 2018
while True:
    try:
        month = int(input('Please enter the month as a number\n'))
        break
    except ValueError:
        print('Please try again')
while True:
    try:
        day = int(input('Please enter the day\n'))
        break
    except ValueError:
        print('Please try again')


#Open Runs (export from database)
openRun = [('112', 'dtc/dtc', '05:05 - 13:30'),
           ('1117', 'dtc/dtc', '05:10 - 17:00'),
           ('113', 'delWebb/dtc', '05:10 - 13:40'),
           ('116', 'delWebb/delWebb', '05:15 - 14:00'),
           ('115', 'dtc/dtc', '06:00 - 15:00'),
           ('111', 'dtc/delWebb', '08:00 - 17:00'),
           ('108','delSat/delWebb', '12:00 - 21:00'),
           ('106', 'delSat/delWebb', '12:00 - 21:30')]

#List of All Drivers (export from database)
operator = [(153, 'plumb', 'extraboard'),
            (163, 'burke', 'extraboard'),
            (179, 'stefanovich', 'extraboard'),
            (192, 'edward', 'extraboard'),
            (201, 'henderson', 'extraboard'),
            (202, 'zimmerman', 'extraboard'),
            (211, 'burgett', 'extraboard'),
            (221, 'wiedemeier', 'extraboard'),
            (223, 'ayala', 'extraboard'),
            (225, 'sherrod', 'extraboard'),
            (226, 'fuchs', 'extraboard'),
            (229, 'cheaqui', 'extraboard'),
            (233, 'parker', 'extraboard'),
            (234, 'martinez', 'extraboard'),
            (232, 'Schaffer', '186'),
            (230, 'Smith', 'vacation'),
            (228, 'Foyle', '173')]
operator = sorted(operator)

#Number of Days Monday Through Friday Excluding Holidays, to be Used in Calculating the Redline Order
def numberDaysMF(year, month, day):
    import datetime
    startDate = datetime.date(2018, 9, 3)
    date_configuring = datetime.date(year, month, day)
    daydiff = date_configuring.weekday() - startDate.weekday()
    if datetime.date(2018, 12, 25) <= date_configuring:
        daydiff = daydiff - 3
    elif datetime.date(2018, 11, 22) <= date_configuring:
        daydiff = daydiff - 2
    elif datetime.date(2018, 9, 3) <= date_configuring:
        daydiff = daydiff - 1
    days = int(((date_configuring - startDate).days - daydiff) / 7 * 5 + min(daydiff, 5) - (max(date_configuring.weekday() - 4, 0) % 5))
    return days

numDays = numberDaysMF(year, month, day)

# Add Number of Drivers on Redline
def addBoard(operator):
    board = 0
    for driver in operator:
        board = sum(1 for x in operator if 'extraboard' in x) + sum(1 for x in operator if 'Vacation Relief' in x)
        vacation = sum(1 for x in operator if 'vacation' in x or 'sick' in x)
        board = board - vacation
    return board
boardNumber = addBoard(operator)

# Calculates Which Operators are a Part of the Redline
def redlineOp(operator):
    x = []
    for driver in operator:
        if 'sick' and 'vacation' not in driver and 'extraboard'in driver or 'Vacation Relief' in driver:
            x.append(driver[:2])
    return x

redOp = redlineOp(operator)

#Assign Open Work to Available ExtraBoard in Redline Order
def assignOpenWork(openRun, redLineOrder):
    assignment = []
    assignment = [redLineOrder[ix] + openRun[ix] for ix in range(len(openRun))]
    return assignment

# Assign Report Time to Remaining ExtraBoard Operators in Redline Order
def assignRepTimes(repOps, repTimes):
    assignment = [repOps[ix] + repTimes[ix] for ix in range(len(repTimes))]
    return assignment

# Number of ExtraBoard Operators on Report
def reportOperators():
    numReportOperators = len(redlineOp(operator))-len(openRun)
    return numReportOperators

reportOps = reportOperators()

# Calculate Report Times Based on Number of Report Operators
def reportTimes(reportOperators):
    if reportOperators == 0:
        list = 0
    elif reportOperators == 1:
        list = [('05:05', 'DelWebb')]
    elif reportOperators == 2:
        list = [('05:05', 'DelWebb'), ('05:15', 'DelWebb')]
    elif reportOperators == 3:
        list = [('05:05', 'DelWebb'), ('05:15', 'DelWebb'), ('05:25', 'DelWebb')]
    elif reportOperators == 4:
        list = [('05:05', 'DelWebb'), ('05:15', 'DelWebb'), ('05:25', 'DelWebb'), ('08:25', 'DelWebb')]
    elif reportOperators == 5:
        list = [('05:05', 'DelWebb'), ('05:15', 'DelWebb'), ('05:25', 'DelWebb'), ('08:25', 'DelWebb'), ('10:30', 'DelWebb')]
    elif reportOperators == 6:
        list = [('05:05', 'DelWebb'), ('05:15', 'DelWebb'), ('05:25', 'DelWebb'), ('08:25', 'DelWebb'), ('10:30', 'DelWebb'), ('11:30', 'DelWebb')]
    elif reportOperators == 7:
        list = [('05:05', 'DelWebb'), ('05:15', 'DelWebb'), ('05:25', 'DelWebb'), ('08:25', 'DelWebb'), ('10:30', 'DelWebb'), ('11:30', 'DelWebb'), ('12:30', 'DelWebb')]
    elif reportOperators == 8:
        list = [('05:05', 'DelWebb'), ('05:15', 'DelWebb'), ('05:25', 'DelWebb'), ('08:25', 'DelWebb'), ('10:30', 'DelWebb'), ('11:30', 'DelWebb'), ('12:30', 'DelWebb'), ('13:30', 'DelWebb')]
    return list

repTimes = reportTimes(reportOperators())

# assign order of operators by redline and date (e.g. (Current_date-beginning_date-weekends-holidays)%number_of_operators...
redLineOrder = (redlineOp(operator)[+numberDaysMF(year, month, day)%boardNumber:] + redlineOp(operator)[:+numberDaysMF(year, month, day)%boardNumber])

assignedRuns = assignOpenWork(openRun, redLineOrder)

# Group Variables to Make it Easier to Work With and Follow
assignedWork = assignOpenWork(openRun, redLineOrder)
repOps = redLineOrder[-reportOperators():]

assignedReport = assignRepTimes(repOps, repTimes)

assignedTotalWork = assignedWork + assignedReport
print(assignedTotalWork)