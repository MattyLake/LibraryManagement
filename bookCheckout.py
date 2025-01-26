import datetime

from database import addCheckoutToLog


def checkoutBook(memberID, bookID, status):
    entry = ""
    print(status)
    if status == "CheckOut":  # Adds checkout date for checkout
        entry = str(bookID) + ", " + str(memberID) + ", " + str(datetime.datetime.today().strftime("[%d,%m,20%y]"))
    elif status == "Reservation":  # Adds no checkout date for reservation
        entry = str(bookID) + ", " + str(memberID)
    addCheckoutToLog(entry)
