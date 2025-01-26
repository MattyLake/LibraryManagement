Matthew Lakin - F222199 - 15/12/2022

To start the application, you need to make sure that all the files including
menu.py
bookSearch.py
bookCheckout.py
bookReturn.py
bookSelect.py
logfile.txt
Book_Info.txt
are all in the same filespace.
The matplotlib module is also required to run this module

To run the application, run the menu.py file.


Book Searching:
Type the title of the book into the search term textbox
and, it will automatically bring up appropriate results.
It will also show the book ID and other information.

Book Checkout:
To check out a book, you need to enter a valid member ID
which needs to be inbetween 1000 and 9999. A valid book
ID also needs to be entered. Depending on if it's
available or not means if you will have to reserve it.

Book Return:
To return a book, enter the bookID of the book to be
returned. If the book is reserved, the memberID of the
member who has reserved it next will appear. There is
validation in place, so you cant return a book that
never got checked out.

Book Selection:
The pie chart refers to the top genres of the past 40
books that has been taken out of the library. Using
these ratios and the budget, a separate budget for each
genre is recommended. The top books are also recommended
to buy more copies. This is also determined by the budget.