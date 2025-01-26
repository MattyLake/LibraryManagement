import datetime


def getNumberOfBooks():
    file = open("Book_Info.txt", "r")
    length = len(file.readlines())
    file.close()
    return length


def getBookInfo(bookID):  # [0]: ID, [1]: Genre, [2]: Title, [3]: Author, [4]: Price, [5]:Purchase Date
    file = open("Book_Info.txt", "r")
    for line in file.readlines():
        if int(line.split(", ")[0]) == int(bookID):
            return line.split(", ")
        file.close()
    return None


def getListOfBookIDs():
    books = []
    file = open("Book_Info.txt", "r")
    for line in file.readlines():
        if line.split(", ")[0] not in books:
            books.append(int(line.split(", ")[0]))
    file.close()
    return books


def getReturned(bookID):  # Returns "✓" if on site, "✕" if checked out or reserved
    file = open("logfile.txt", "r")
    entries = []
    for line in file.readlines():
        if bookID == int(line.split(", ")[0]):
            entries.append(line)
    file.close()
    if len(entries) == 0:
        return "✓"
    latestEntry = entries[len(entries) - 1]
    match(len(latestEntry.split(", "))):
        case 4:
            return "✓"
        case 3:
            return "✕"
        case 2:
            return "✕"


def addCheckoutToLog(entry):
    file = open("logfile.txt", "a")
    file.write("\n"+entry)
    file.close()


def checkForLatestCheckout(bookID):
    first = True
    latestCheckoutLine = -1
    firstReservationLine = -1
    index = 0
    file = open("logfile.txt", "r")
    for line in file.readlines():
        if int(bookID) == int(line.split(", ")[0]) and len(line.split(", ")) == 3:  # Updates if checkout
            latestCheckoutLine = index
        elif int(bookID) == int(line.split(", ")[0]) and len(line.split(", ")) == 2 and first is True:  # Updates if reservation
            firstReservationLine = index
            first = False
        index += 1
    file.close()
    if firstReservationLine == -1 and latestCheckoutLine == -1:
        return []
    elif firstReservationLine == -1 and latestCheckoutLine != -1:
        return [latestCheckoutLine]
    else:
        return [latestCheckoutLine, firstReservationLine]


def addReturnToLog(lines):
    file = open("logfile.txt", "r")
    data = file.readlines()
    file.close()

    if len(lines) == 2:  # Reservation
        data[lines[0]] = data[lines[0]].replace("\n", "") + ", " + datetime.datetime.today().strftime("[%d,%m,20%y]"+"\n")
        data[lines[1]] = data[lines[1]].replace("\n", "") + ", " + datetime.datetime.today().strftime("[%d,%m,20%y]"+"\n")
    elif len(lines) == 1:  # Checkout
        data[lines[0]] = data[lines[0]].replace("\n", "") + ", " + datetime.datetime.today().strftime("[%d,%m,20%y]"+"\n")

    file = open("logfile.txt", "w")
    for line in data:
        file.write(line)
    file.close()

    if len(lines) == 2:
        memberIDOfReservation = data[lines[1]].split(", ")[1]
        return memberIDOfReservation
    else:
        return None


def getTopAttributesAndValues(bookOrGenre):  # Genre = 1, Book = 2
    file = open("logfile.txt", "r")
    data = file.readlines()
    file.close()

    attributes = []
    values = []
    for i in range(0, 41):
        attribute = getBookInfo(data[len(data)-1-i].split(", ")[0])[bookOrGenre]
        if attribute in attributes:
            values[attributes.index(attribute)] += 1
        else:
            attributes.append(attribute)
            values.append(1)

    valuesRanked = sorted(values)
    valuesRanked.reverse()

    topGenres = []
    topValues = []

    for i in range(0, 5):
        count = valuesRanked[i]
        topGenres.append(attributes[values.index(count)])
        topValues.append(values[values.index(count)])
        if bookOrGenre == 2:
            attributes[values.index(count)] = None
            values[values.index(count)] = None

    return [topGenres, topValues]


def getBookIDFromTitle(title):
    file = open("Book_Info.txt", "r")
    for line in file.readlines():
        if line.split(", ")[2] == title:
            file.close()
            return line.split(", ")[0]


def getGenreFromTitle(title):
    file = open("Book_Info.txt", "r")
    for line in file.readlines():
        if line.split(", ")[2] == title:
            file.close()
            return line.split(", ")[1]


def getAverageGenreCost(genre):
    file = open("Book_Info.txt", "r")
    prices = []
    for line in file.readlines():
        if line.split(", ")[1] == genre:
            prices.append(float(line.split(", ")[4]))
    return sum(prices)/len(prices)
