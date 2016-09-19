# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Altis-Launcher.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_AltisLauncher(object):
    def setupUi(self, AltisLauncher):
        AltisLauncher.setObjectName(_fromUtf8("AltisLauncher"))
        AltisLauncher.resize(778, 427)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(AltisLauncher.sizePolicy().hasHeightForWidth())
        AltisLauncher.setSizePolicy(sizePolicy)
        AltisLauncher.setMaximumSize(QtCore.QSize(778, 427))
        AltisLauncher.setFocusPolicy(QtCore.Qt.TabFocus)
        self.Frame = QtGui.QWidget(AltisLauncher)
        self.Frame.setObjectName(_fromUtf8("Frame"))
        self.LoginButton = QtGui.QPushButton(self.Frame)
        self.LoginButton.setGeometry(QtCore.QRect(530, 250, 131, 41))
        self.LoginButton.setToolTip(_fromUtf8(""))
        self.LoginButton.setAutoFillBackground(False)
        self.LoginButton.setObjectName(_fromUtf8("LoginButton"))
        self.QuitButton = QtGui.QPushButton(self.Frame)
        self.QuitButton.setGeometry(QtCore.QRect(700, 400, 75, 23))
        self.QuitButton.setObjectName(_fromUtf8("QuitButton"))
        self.UsernameText = QtGui.QLabel(self.Frame)
        self.UsernameText.setGeometry(QtCore.QRect(400, 170, 81, 21))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Segoe UI Black"))
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.UsernameText.setFont(font)
        self.UsernameText.setObjectName(_fromUtf8("UsernameText"))
        self.PasswordText = QtGui.QLabel(self.Frame)
        self.PasswordText.setGeometry(QtCore.QRect(400, 200, 81, 21))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Segoe UI Black"))
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.PasswordText.setFont(font)
        self.PasswordText.setObjectName(_fromUtf8("PasswordText"))
        self.TitleText = QtGui.QLabel(self.Frame)
        self.TitleText.setGeometry(QtCore.QRect(380, 30, 411, 91))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("MV Boli"))
        font.setPointSize(48)
        font.setBold(True)
        font.setWeight(75)
        self.TitleText.setFont(font)
        self.TitleText.setObjectName(_fromUtf8("TitleText"))
        self.Changelog = QtWebKit.QWebView(self.Frame)
        self.Changelog.setGeometry(QtCore.QRect(0, 0, 381, 421))
        self.Changelog.setUrl(QtCore.QUrl(_fromUtf8("http://beesbeesbees.com/")))
        self.Changelog.setObjectName(_fromUtf8("Changelog"))
        self.UsernameEntry = QtGui.QLineEdit(self.Frame)
        self.UsernameEntry.setGeometry(QtCore.QRect(480, 170, 251, 20))
        self.UsernameEntry.setObjectName(_fromUtf8("UsernameEntry"))
        self.PasswordEntry = QtGui.QLineEdit(self.Frame)
        self.PasswordEntry.setGeometry(QtCore.QRect(480, 200, 251, 20))
        self.PasswordEntry.setInputMask(_fromUtf8(""))
        self.PasswordEntry.setFrame(True)
        self.PasswordEntry.setEchoMode(QtGui.QLineEdit.Password)
        self.PasswordEntry.setObjectName(_fromUtf8("PasswordEntry"))
        AltisLauncher.setCentralWidget(self.Frame)

        self.retranslateUi(AltisLauncher)
        QtCore.QMetaObject.connectSlotsByName(AltisLauncher)
        AltisLauncher.setTabOrder(self.LoginButton, self.Changelog)
        AltisLauncher.setTabOrder(self.Changelog, self.QuitButton)

    def retranslateUi(self, AltisLauncher):
        AltisLauncher.setWindowTitle(_translate("AltisLauncher", "Project Altis Launcher", None))
        AltisLauncher.setAccessibleName(_translate("AltisLauncher", "Project Altis Launcher", None))
        AltisLauncher.setAccessibleDescription(_translate("AltisLauncher", "Project Altis Launcher", None))
        self.LoginButton.setText(_translate("AltisLauncher", "Login", None))
        self.QuitButton.setText(_translate("AltisLauncher", "Quit", None))
        self.UsernameText.setText(_translate("AltisLauncher", "Username:", None))
        self.PasswordText.setText(_translate("AltisLauncher", "Password:", None))
        self.TitleText.setText(_translate("AltisLauncher", "Project Altis", None))

from PyQt4 import QtWebKit
