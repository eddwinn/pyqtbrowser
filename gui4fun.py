import sys, pickle
from PyQt4.QtCore import QUrl
from PyQt4 import QtGui, QtCore
from PyQt4.QtWebKit import *

from functools import partial


# a = {1:"www.yahoo.com",2:"www.ebay.com"}
#
#
# b = open("bookmarks.txt", "wb")
# pickle.dump(a, b)
# #bookmark = pickle.load(b)
#
# b.close()

pickle_in = open("bookmarks.txt", "rb")
bookmarks = pickle.load(pickle_in)
print(bookmarks)
print(bookmarks[2])

url = ""

class Main(QtGui.QMainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.initUI(mapping=bookmarks)

    def initUI(self, mapping):

        global bookmarks

        self.centralwidget = QtGui.QWidget(self)

        self.line = QtGui.QLineEdit(self)
        self.line.setMinimumSize(1150,30)
        self.line.setStyleSheet("font-size:15px;")

        self.enter = QtGui.QPushButton(self)
        self.enter.resize(0,0)
        self.enter.clicked.connect(self.Enter)
        self.enter.setShortcut("Return")

        self.reload = QtGui.QPushButton("↻",self)
        self.reload.setMinimumSize(35,30)
        self.reload.setShortcut("F5")
        self.reload.setStyleSheet("font-size:23px;")
        self.reload.clicked.connect(self.Reload)




        self.back = QtGui.QPushButton("◀",self)
        self.back.setMinimumSize(35,30)
        self.back.setStyleSheet("font-size:23px;")
        self.back.clicked.connect(self.Back)

        self.forw = QtGui.QPushButton("▶",self)
        self.forw.setMinimumSize(35,30)
        self.forw.setStyleSheet("font-size:23px;")
        self.forw.clicked.connect(self.Forward)



        self.book = QtGui.QPushButton("☆",self)
        self.book.setMinimumSize(35,30)
        self.book.clicked.connect(self.Bookmark)
        self.book.setStyleSheet("font-size:18px;")

        self.pbar = QtGui.QProgressBar()
        self.pbar.setMaximumWidth(120)

        self.web = QWebView(loadProgress = self.pbar.setValue, loadFinished = self.pbar.hide, loadStarted = self.pbar.show, titleChanged = self.setWindowTitle)
        self.web.setMinimumSize(400,300)
        self.web.load(QUrl('http://www.google.com'))



        self.bokbar = QtGui.QPushButton("Y", self)
        self.bokbar.clicked.connect(self.BookmarkBar)


        self.list = QtGui.QComboBox(self)
        self.list.setMinimumSize(35,30)

        for i in bookmarks:
            self.list.addItem(str(i))

        self.list.activated[str].connect(self.handleBookmarks)
        self.list.view().setSizePolicy(QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Minimum)




        self.web.urlChanged.connect(self.UrlChanged)

        self.web.page().linkHovered.connect(self.LinkHovered)


#_________________________________________________________________________
#(down starting from top, from left, continuing, how many rows it spas across)

        grid = QtGui.QGridLayout()
        grid.setSpacing(5)

        grid.addWidget(self.back,  0,  0, 1, 1)
        grid.addWidget(self.line,  0,  3, 1, 1)
        grid.addWidget(self.book,  0,  4, 1, 1)
        grid.addWidget(self.forw,  0,  1, 1, 1)
        grid.addWidget(self.bokbar,1,  0, 1, 1)
        grid.addWidget(self.reload,0,  2, 1, 1)
        grid.addWidget(self.list,  0,  5, 1, 1)
        grid.addWidget(self.web,   2,  0, 1, 6)


        self.centralwidget.setLayout(grid)
#_________________________________________________________________________
#---------Window settings --------------------------------

        self.setGeometry(50,50,1360,768)
        self.setWindowTitle("PySurf")
        self.setWindowIcon(QtGui.QIcon(""))
        self.setStyleSheet("background-color:")

        self.status = self.statusBar()
        self.status.addPermanentWidget(self.pbar)
        self.status.hide()

        self.setCentralWidget(self.centralwidget)
#_________________________________________________________________________
    def Enter(self):
        global url
        global bookmarks

        url = self.line.text()

        http = "http://"
        www = "www."

        if www in url and http not in url:
            url = http + url

        elif "." not in url:
            url = "http://www.google.com/search?q="+url

        elif http in url and www not in url:
            url = url[:7] + www + url[7:]

        elif http and www not in url:
            url = http + www + url


        self.line.setText(url)

        self.web.load(QtCore.QUrl(url))

        if url in bookmarks:
            self.book.setText("★")

        else:
            self.book.setText("☆")

        self.status.show()

    def Bookmark(self):
        global url
        global bookmarks

        #bookmarks.append(url)

        b = open("bookmarks.txt","wb")
        pickle.dump(bookmarks,b)
        b.close()

        self.list.addItem(url)
        self.book.setText("★")

    def handleBookmarks(self,choice):
        global url

        url = choice
        self.line.setText(url)
        self.Enter()

    def Back(self):
        self.web.back()

    def Forward(self):
        self.web.forward()

    def Reload(self):
        self.web.reload()

    def UrlChanged(self):
        self.line.setText(self.web.url().toString())

    def LinkHovered(self,l):
        self.status.showMessage(l)

    def BookmarkBar(self):
        i = 0
        for b in bookmarks:
            btn1 = QtGui.QPushButton(b, self)
            btn1.move(30, 50 + i)
            i += 30
            btn1.clicked.connect(self.buttonClicked)
            btn1.show()
        self.resize(self.width(), 50 + i)



#_________________________________________________________________________

def main():
    app = QtGui.QApplication(sys.argv)
    main= Main()
    main.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()