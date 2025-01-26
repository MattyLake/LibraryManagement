from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from database import getTopAttributesAndValues, getBookInfo, getBookIDFromTitle


def createPiChart(fontColour):
    data = getTopAttributesAndValues(1)  # Gets data for chart
    fig = Figure()
    ax = fig.add_subplot(111)
    plt.rcParams['text.color'] = fontColour
    ax.pie(data[1], autopct='%1.1f%%', pctdistance=1.4, startangle=90, textprops={'fontsize': 6})
    ax.legend(data[0], bbox_to_anchor=(0.5, 0.5), title="Top Genres", loc='center', fontsize=8)
    return fig  # Returns pie chart to main file


def getTopAttributes(bookOrGenre):
    return getTopAttributesAndValues(bookOrGenre)[0]


def getTopValues(bookOrGenre):
    return getTopAttributesAndValues(bookOrGenre)[1]


def calculateHowManyBooksToBeBought(bookTitle, weighting,  budget):
    bookPrice = float(getBookInfo(getBookIDFromTitle(bookTitle))[4])
    numberOfBooks = 0.1 * float(budget) * float(weighting) / bookPrice
    return round(numberOfBooks, 0)
