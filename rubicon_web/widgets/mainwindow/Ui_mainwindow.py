# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Code\Rubicon-Web\rubicon_web\widgets\mainwindow\UI_mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.8
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1112, 539)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setStyleSheet("QWidget {\n"
"    background-color: /bg_color/;\n"
"}")
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.centralwidget_layout.setContentsMargins(0, 0, 0, 0)
        self.centralwidget_layout.setSpacing(0)
        self.centralwidget_layout.setObjectName("centralwidget_layout")
        self.main_layout = QtWidgets.QSplitter(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.main_layout.sizePolicy().hasHeightForWidth())
        self.main_layout.setSizePolicy(sizePolicy)
        self.main_layout.setOrientation(QtCore.Qt.Horizontal)
        self.main_layout.setHandleWidth(0)
        self.main_layout.setObjectName("main_layout")
        self.bookmarks_sidebar = QtWidgets.QTreeWidget(self.main_layout)
        self.bookmarks_sidebar.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bookmarks_sidebar.sizePolicy().hasHeightForWidth())
        self.bookmarks_sidebar.setSizePolicy(sizePolicy)
        self.bookmarks_sidebar.setObjectName("bookmarks_sidebar")
        self.bookmarks_sidebar.headerItem().setText(0, "1")
        self.centralwidget_layout.addWidget(self.main_layout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1112, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
