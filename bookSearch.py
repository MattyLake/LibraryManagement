from database import getBookInfo, getListOfBookIDs


def searchIDs(query):  # Create list of IDs of books that match the search criteria
    entries = []
    listOfBookIDs = getListOfBookIDs()
    for bookID in listOfBookIDs:
        if query.get().lower() in getBookInfo(bookID)[2].lower():
            entries.append(bookID)
    return entries
