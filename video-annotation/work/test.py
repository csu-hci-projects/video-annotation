# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(230, 100, 483, 402))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.videoLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.videoLayout.setContentsMargins(0, 0, 0, 0)
        self.videoLayout.setObjectName("videoLayout")
        self.sourceVideo = QtWidgets.QGraphicsView(self.horizontalLayoutWidget)
        self.sourceVideo.setMinimumSize(QtCore.QSize(300, 300))
        self.sourceVideo.setObjectName("sourceVideo")
        self.videoLayout.addWidget(self.sourceVideo)
        self.targetVIdeo = QtWidgets.QGraphicsView(self.horizontalLayoutWidget)
        self.targetVIdeo.setObjectName("targetVIdeo")
        self.videoLayout.addWidget(self.targetVIdeo)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

