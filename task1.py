import re
from datetime import datetime
import sys
import Countries
import functions


if __name__ == '__main__':
    argumentLine = sys.argv[1::]

    days = cases = deaths = month = country = continent = ""
    summed = byDate = byNumbers = descending = ascending = test = False
    days = []

    file_name = "Covid.txt"

    if argumentLine[0].upper() in Countries.countries.values():
        country = argumentLine[0]
    elif argumentLine[0].upper() in Countries.continents:
        continent = argumentLine[0]
    else:
        raise Exception("Given country or continent is not in the file")

    if re.search("DEATHS", argumentLine[1]):
        cases = False
        deaths = True
    elif re.search("CASES", argumentLine[1]):
        cases = True
        deaths = False
    else:
        raise Exception("Invalid argument given")

    if re.search("SUM", argumentLine[2]):
        summed = True
    elif re.search("LINER", argumentLine[2]):
        summed = False
        ascending = True
    elif re.search("LINEM", argumentLine[2]):
        summed = False
        descending = True
    else:
        raise Exception("Invalid argument given")

    if re.search("DATE", argumentLine[3]):
        byDate = True
    elif re.search("NUM", argumentLine[3]):
        byNumbers = True
    elif len(argumentLine[3]) == 10:
        days = [argumentLine[3], argumentLine[3]]
        functions.dayValidation(days)
    elif len(argumentLine[3]) <= 2:
        month = argumentLine[3]
        functions.monthValidation(month)
    else:
        raise Exception("Invalid argument given")

    if argumentLine[3] == "DATE" or argumentLine[3] == "NUM":
        if len(argumentLine[4]) == 10:
            days = [argumentLine[4], argumentLine[4]]
            functions.dayValidation(days)
            if len(argumentLine) == 6:
                days = [argumentLine[4], argumentLine[5]]
                functions.dayValidation(days)
        elif len(argumentLine[4]) <= 2:
            month = argumentLine[4]
            functions.monthValidation(month)
    else:
        if len(argumentLine) == 5:
            if len(argumentLine[4]) == 10:
                days = [argumentLine[3], argumentLine[4]]
                functions.dayValidation(days)

    listOfDays = functions.processData(file_name, days, cases, summed, month, country, continent)

    if byDate and ascending:
        listOfDays = sorted(listOfDays, key=lambda day_data: datetime.strptime(day_data[0], "%d.%m.%Y"))
    elif byDate and descending:
        listOfDays = sorted(listOfDays, key=lambda day_data: datetime.strptime(day_data[0], "%d.%m.%Y"),
                            reverse=True)
    elif byNumbers and ascending:
        if cases:
            listOfDays = sorted(listOfDays, key=lambda day_data: day_data[2])
        elif deaths:
            listOfDays = sorted(listOfDays, key=lambda day_data: day_data[3])
    elif byNumbers and descending:
        if cases:
            listOfDays = sorted(listOfDays, key=lambda day_data: day_data[2], reverse=True)
        elif deaths:
            listOfDays = sorted(listOfDays, key=lambda day_data: day_data[3], reverse=True)

    if not summed:
        print("DATE\tMONTH\tCASES\tDEATHS\tCOUNTRY\tCONTINENT")
        for i in listOfDays:
            for j in i:
                print("%s" % j, end="\t\t")
            print("\n", end="")
