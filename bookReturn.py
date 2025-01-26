from database import checkForLatestCheckout, addReturnToLog, getBookInfo


def returnBook(bookID):
    checkoutLines = checkForLatestCheckout(bookID)
    if len(checkoutLines) != 0:
        memberIDReserved = addReturnToLog(checkoutLines)
        # return [Book Name Returned, Member ID of reservation]
        if memberIDReserved is None:
            return [getBookInfo(bookID)[2]]
        else:
            return [getBookInfo(bookID)[2], memberIDReserved]
    else:
        return None
