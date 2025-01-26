import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from database import getBookInfo, getNumberOfBooks, getReturned
from bookSearch import searchIDs
from bookCheckout import checkoutBook
from bookReturn import returnBook
from bookSelect import createPiChart, getTopValues, getTopAttributes, calculateHowManyBooksToBeBought

# Constants
backgroundColour = "Gray"
highlightColour = "LightGray"
textColour1 = "MidnightBlue"
textColour2 = "MediumBlue"

window = tk.Tk()
window.title("Book Management")
window.config(bg="Gray25")

title = tk.Label(window, text="Book Management - F222199", justify="center",
                 bg="Gray25", fg=textColour1, font=("Arial", 20, "bold", "underline"))
title.grid(column=0, row=0, columnspan=100)

# Frame 1: Book Search ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
bookSearchFrame = tk.Frame(window, relief=tk.GROOVE, borderwidth=3, bg=backgroundColour)
bookSearchFrame.grid(column=0, row=1, rowspan=2, padx=10, pady=10, sticky=tk.NSEW)

titleLabel = tk.Label(bookSearchFrame, text="Search for a Book                                         Enter Term:",
                      bg=backgroundColour, fg=textColour1, font=("Ariel", 14, "bold"))
titleLabel.grid(column=0, row=0)

resultArea = tk.Frame(bookSearchFrame)
resultArea.grid(column=0, row=1, columnspan=2)


def clearResultArea():
    gridSlaves = resultArea.grid_slaves()
    for item in gridSlaves:
        item.destroy()


def showSearchResults(query):
    bookIDs = searchIDs(query)
    clearResultArea()
    renderBookEntries(bookIDs)


def renderBookEntries(bookIDs):
    fields = ["ID", "Genre", "Title", "Author", "Price", "Purchase Date", "Available?"]
    k = 0
    cols = []
    rows = []
    for field in fields:
        e = tk.Label(resultArea, relief=tk.SUNKEN, text=field, font=("Arial", 15), fg=textColour1, bg=highlightColour)
        e.grid(row=0, column=k, sticky=tk.NSEW)
        cols.append(e)
        k += 1
    rows.append(cols)
    rows = []
    for i in range(0, len(bookIDs)):
        cols = []
        for j in range(7):
            if j == 4:
                textStore = "£"+getBookInfo(bookIDs[i])[j]
                e = tk.Label(resultArea, relief=tk.SUNKEN, text=textStore, wraplength=200,
                             bg=highlightColour, fg=textColour2)
            elif j == 5:
                textStore = getBookInfo(bookIDs[i])[j]
                e = tk.Label(resultArea, relief=tk.SUNKEN, text=textStore.replace("\n",""), wraplength=200,
                             bg=highlightColour, fg=textColour2)
            elif j == 6:
                e = tk.Label(resultArea, relief=tk.SUNKEN, text=getReturned(bookIDs[i]), wraplength=200,
                             bg=highlightColour, fg=textColour2)
            else:
                textStore = getBookInfo(bookIDs[i])[j]
                e = tk.Label(resultArea, relief=tk.SUNKEN, text=textStore, wraplength=200,
                             bg=highlightColour, fg=textColour2)
            e.grid(row=i+1, column=j, sticky=tk.NSEW)
            cols.append(e)
        rows.append(cols)


sv = tk.StringVar()  # Listens for change in the titleEntry object and runs showSearchResults() every time
sv.trace("w", lambda name, index, mode, sv=sv: showSearchResults(sv))
titleEntry = tk.Entry(bookSearchFrame, textvariable=sv, font=("Ariel", 12),
                      bg=highlightColour, fg=textColour1)
titleEntry.grid(column=1, row=0, sticky=tk.NSEW)

showSearchResults(tk.StringVar())

# Frame 2: Book Checkout ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
bookCheckoutFrame = tk.Frame(window, relief=tk.GROOVE, borderwidth=3, bg=backgroundColour)
bookCheckoutFrame.grid(column=1, row=1, padx=10, pady=10, sticky=tk.NSEW)

bookCheckoutTitle = tk.Label(bookCheckoutFrame, text="Check out a Book",
                             bg=backgroundColour, fg=textColour1, font=("Ariel", 14, "bold"))
bookCheckoutTitle.grid(column=0, columnspan=2, row=0, sticky=tk.NSEW)

memberIDLabel = tk.Label(bookCheckoutFrame, text="Member ID:", bg=backgroundColour, fg=textColour2)
memberIDLabel.grid(column=0, columnspan=2, row=1, sticky=tk.NSEW)

memberIDEntry = tk.Entry(bookCheckoutFrame,  font=("Ariel", 20), width=8,
                         bg=highlightColour, fg=textColour1)
memberIDEntry.grid(column=0, columnspan=2, row=2, sticky=tk.NSEW)

bookIDLabelCheckout = tk.Label(bookCheckoutFrame, text="Book ID:", bg=backgroundColour, fg=textColour2)
bookIDLabelCheckout.grid(column=0, columnspan=2, row=3, sticky=tk.NSEW)

bookIDEntryCheckout = tk.Entry(bookCheckoutFrame, font=("Ariel", 20), width=8,
                               bg=highlightColour, fg=textColour1)
bookIDEntryCheckout.grid(column=0, columnspan=2, row=4, sticky=tk.NSEW)


def validateEntries(memberID, bookID, status):
    integers = True
    inRange = False
    comment = []
    verifyMemberID = 0
    verifyBookID = 0

    try:  # Validation that checks if memberID and bookID is numeric
        verifyMemberID = int(memberID)
        verifyBookID = int(bookID)
    except ValueError:
        integers = False

    # Checks that values of memberID and bookID is valid
    if 1 <= verifyBookID <= getNumberOfBooks() and 1000 <= verifyMemberID <= 9999:
        inRange = True

    if inRange is False:
        comment.append("Values not in range")
    if integers is False:
        comment.append("Invalid Values")
    if getReturned(verifyBookID) == "✕" and status == "CheckOut":
        comment.append("Book is unavailable. Reservable")
    if getReturned(verifyBookID) == "✓" and status == "Reservation":
        comment.append("Book is available, use Check-Out")
    if inRange is False or integers is False or (getReturned(verifyBookID) == "✕" and status == "CheckOut") or\
            (getReturned(verifyBookID) == "✓" and status == "Reservation"):
        commentString = ""
        for part in comment:
            commentString = commentString+part+"\n"
        bookCheckoutComment.config(text=commentString[:len(commentString)-1])

    if inRange is True and integers is True:
        if getReturned(verifyBookID) == "✓" and status == "CheckOut":
            checkoutBook(verifyMemberID, verifyBookID, status)
            comment = ("The book \'"+getBookInfo(verifyBookID)[2]+"\' has been successfully checked out")
            bookCheckoutComment.config(text=comment)
        if getReturned(verifyBookID) == "✕" and status == "Reservation":
            checkoutBook(verifyMemberID, verifyBookID, status)
            comment = ("The book \'" + getBookInfo(verifyBookID)[2] + "\' has been successfully reserved")
            bookCheckoutComment.config(text=comment)

    sv.set(titleEntry.get())  # Updates the table for new availability


checkoutButton = tk.Button(bookCheckoutFrame, text="Check out Book",
                           command=lambda: validateEntries(memberIDEntry.get(), bookIDEntryCheckout.get(), "CheckOut"),
                           bg=highlightColour, fg=textColour1)
checkoutButton.grid(column=0, row=5, sticky=tk.NSEW, padx=5, pady=5)

reserveButton = tk.Button(bookCheckoutFrame, text="Reserve Book",
                          command=lambda: validateEntries(memberIDEntry.get(), bookIDEntryCheckout.get(), "Reservation"),
                          bg=highlightColour, fg=textColour1)
reserveButton.grid(column=1, row=5, sticky=tk.NSEW, padx=5, pady=5)

bookCheckoutComment = tk.Label(bookCheckoutFrame, bg=highlightColour, fg=textColour1, wraplength=200)
bookCheckoutComment.grid(column=0, row=6, columnspan=2, sticky=tk.NSEW, padx=5, pady=5)

bookCheckoutFrame.grid_rowconfigure(0, weight=1)
for i in range(1, 7):
    bookCheckoutFrame.grid_rowconfigure(i, weight=3)
for i in range(0, 2):
    bookCheckoutFrame.grid_columnconfigure(i, weight=1)

# Frame 3: Book Return ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
bookReturnFrame = tk.Frame(window, relief=tk.GROOVE, borderwidth=3, bg=backgroundColour)
bookReturnFrame.grid(column=2, row=1, padx=10, pady=10, sticky=tk.NSEW)

bookReturnTitle = tk.Label(bookReturnFrame, text="Return a book",
                           bg=backgroundColour, fg=textColour1, font=("Ariel", 14, "bold"))
bookReturnTitle.grid(column=0, row=0, sticky=tk.NSEW)

bookIDLabelReturn = tk.Label(bookReturnFrame, text="Book ID:", bg=backgroundColour, fg=textColour2)
bookIDLabelReturn.grid(column=0, row=1, sticky=tk.NSEW)

bookIDEntryReturn = tk.Entry(bookReturnFrame, font=("Ariel", 28), width=8,
                              bg=highlightColour, fg=textColour1)
bookIDEntryReturn.grid(column=0, row=2, sticky=tk.NSEW)


def validateReturnBook(bookID):
    try:  # Integer Validation
        bookID = int(bookID)
    except ValueError:
        bookReturnComment.config(text="Invalid Book ID")
        return

    if 1 <= bookID <= getNumberOfBooks():  # In range Validation
        bookNames = returnBook(bookID)
        if type(bookNames) is list:
            if len(bookNames) == 2:  # If reserved
                bookReturnComment.config(text=("The book \'"+bookNames[0]+
                                               "\' has been returned. The member with ID "+bookNames[1]+
                                               " has reserved this book"))
            if len(bookNames) == 1:  # If not reserved
                bookReturnComment.config(text=("The book \'"+bookNames[0]+"\' has been returned."))
        else:  # If not checked out
            bookReturnComment.config(text="Book has not been checked out")
    else:  # If invalid
        bookReturnComment.config(text="Invalid Book ID")


returnBookButton = tk.Button(bookReturnFrame, text="Return Book",
                             command=lambda: validateReturnBook(bookIDEntryReturn.get()),
                             bg=highlightColour, fg=textColour1)
returnBookButton.grid(column=0, row=3, sticky=tk.NSEW, padx=5, pady=5)

bookReturnComment = tk.Label(bookReturnFrame, bg=highlightColour, fg=textColour1, wraplength=200)
bookReturnComment.grid(column=0, row=4, sticky=tk.NSEW, padx=5, pady=5)

bookReturnFrame.grid_rowconfigure(0, weight=1)  # Make the objects larger
for i in range(1, 5):
    bookReturnFrame.grid_rowconfigure(i, weight=4)
bookReturnFrame.grid_columnconfigure(0, weight=1)

# Frame 4: Book Select ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
bookSelectFrame = tk.Frame(window, relief=tk.GROOVE, borderwidth=3, bg=backgroundColour)
bookSelectFrame.grid(column=1, row=2, padx=10, pady=10, columnspan=2, sticky=tk.NSEW)

bookSelectTitle = tk.Label(bookSelectFrame, text="Selecting Books for Purchase Order",
                           bg=backgroundColour, fg=textColour1, font=("Ariel", 14, "bold"))
bookSelectTitle.grid(column=0, row=0, columnspan=3, sticky=tk.NSEW)

budgetLabel = tk.Label(bookSelectFrame, text="Please Enter the Budget:",
                       bg=backgroundColour, fg=textColour1)
budgetLabel.grid(column=0, row=1, sticky=tk.NSEW, padx=5, pady=5)

budgetEntry = tk.Entry(bookSelectFrame, bg=highlightColour, fg=textColour1)
budgetEntry.insert(0, "3000")
budgetEntry.grid(column=1, row=1, sticky=tk.NSEW, padx=5, pady=5)


def budgetButtonClicked(budget):
    comment = "Recommended Spend:\n"
    topGenres = getTopAttributes(1)  # Genre = 1, Book = 2
    topValues = getTopValues(1)
    for i in range(0, len(topGenres)):
        spend = round(topValues[i]/sum(topValues) * int(budget), 2)
        comment = comment+str(i+1)+": "+topGenres[i]+" - £"+str(spend)+"\n"
    comment = comment + "\nBuy More of these books:\n"

    topBooks = getTopAttributes(2)
    topValues = getTopValues(2)

    for i in range(0, len(topBooks)):
        weighting = topValues[i] / sum(topValues)
        numberOfBooks = calculateHowManyBooksToBeBought(topBooks[i], weighting, budget)
        comment = comment+"Buy "+str(int(numberOfBooks))+" copies of "+topBooks[i]+"\n"

    budgetingLabel.config(text=comment)


budgetButton = tk.Button(bookSelectFrame, text="Budget", command=lambda: budgetButtonClicked(budgetEntry.get()),
                         bg=highlightColour, fg=textColour1)
budgetButton.grid(column=2, row=1, sticky=tk.NSEW, padx=5, pady=5)

budgetingLabel = tk.Label(bookSelectFrame, text="1: Fantasy - £3000.33\n1: Fantasy - £3000.33",
                          bg=highlightColour, fg=textColour2)
budgetingLabel.grid(column=2, row=2, sticky=tk.NSEW, padx=5, pady=5)

chart = createPiChart(textColour2)
genrePiChart = FigureCanvasTkAgg(chart, master=bookSelectFrame)
genrePiChart.get_tk_widget().grid(column=0, row=2, columnspan=2, sticky=tk.NSEW, padx=5, pady=5)
genrePiChart.get_tk_widget().config(height=170, width=200)

for i in range(0, 3):
    bookSelectFrame.grid_rowconfigure(i, weight=1)
for i in range(0, 3):
    bookSelectFrame.grid_columnconfigure(i, weight=1)

budgetButtonClicked(budgetEntry.get())



window.mainloop()
