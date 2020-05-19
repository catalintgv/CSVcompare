#-------------------------------------------------------------------------------
# Name:        mainCSV
# Purpose:
#
# Author:      cdpinta
#
# Created:     18.05.2020
# Copyright:   (c) cdpinta 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import sys, os , glob
from os.path import expanduser
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QAction, QMessageBox, QLabel, QTableWidgetItem, QTableWidget
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtGui import *
import csv
from PyQt5.QtWidgets import (QMainWindow, QTextEdit, QFileDialog, QVBoxLayout)
from PyQt5.QtGui import QIcon

class Ui(QtWidgets.QMainWindow):

    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('untitled.ui', self)
        self.setWindowIcon(QIcon('ico.png'))
        self.setWindowTitle('CSV file Reader')
        self.browseFolder.clicked.connect(self.choseDir)
        #self.user.addItems(['a','b'])
        #self.user.addItems[str].connect([self.userList])
        self.user.currentIndexChanged[str].connect(self.getUser)
        self.grad.currentIndexChanged[str].connect(self.getGrad)
        self.celula.currentIndexChanged[str].connect(self.getCelula)
        self.t2.currentIndexChanged[str].connect(self.getZit2)
        self.t1.currentIndexChanged[str].connect(self.getZit1)
        self.listeaza.clicked.connect(self.listeazaTabel)
        #self.pushButton.clicked.connect(self.clearTable)


    def choseDir(self):
        self.input_dir = QFileDialog.getExistingDirectory(None, 'Select a folder:', expanduser(" "))
        #print(input_dir)
        #mylist = [f for f in glob.glob("*.csv")]

        self.myList= []
        self.userList = []
        self.gradList = []
        self.celulaList = []
        self.ziList = []

##        for file in glob.glob(os.path.join(input_dir, '*.csv')):
##            print(file)

        for root, dirs, files in os.walk(self.input_dir, topdown=False):
            for file in files:
                #print(file)
                if file[0].isupper() and file.endswith(".csv"):
                    self.myList.append(file)
                    if file[0:2] not in self.userList:
                        self.userList.append(file[0:2])
                        #print(self.userList)

        self.user.clear()
        self.user.addItems(self.userList)
        self.user.update()

    def getUser(self,u):
        self.cUser = u
        self.gradList.clear()

        for file in self.myList:
            if file[0:2]==u:
                if file[3:7] not in self.gradList:
                    self.gradList.append(file[3:7])

        self.grad.clear()
        self.grad.addItems(self.gradList)
        self.user.update()
        #print(u)

    def getGrad(self,g):
        self.cGrad = g
        b = self.cUser+'_'+self.cGrad
        self.celulaList.clear()

        for file in self.myList:
            if b in file[0:7]:
                if file[8:12] not in self.celulaList:
                    self.celulaList.append(file[8:12])

        self.celula.clear()
        self.celula.addItems(self.celulaList)
        self.celula.update()
        #print(g)

    def getCelula(self,c):
        self.cCelula = c
        d = self.cUser+'_'+self.cGrad+'_'+self.cCelula
        self.ziList.clear()

        for file in self.myList:
            if d in file[0:12]:
                if file[13:20] not in self.ziList:
                    self.ziList.append(file[13:21])

        self.t1.clear()
        self.t1.addItems(self.ziList)
        self.t1.update()

        self.t2.clear()
        self.t2.addItems(self.ziList)
        self.t2.update()

    def getZit2(self, z2):
        self.cZ2 = z2
        #print(z2)

    def getZit1(self, z1):
        self.cZ1 = z1
        #print(z1)

    def listeazaTabel(self):
        try:

            self.csv2= self.input_dir+'/'+self.cUser+'_'+self.cGrad+'_'+self.cCelula+'_'+self.cZ2+'.csv'
            self.csv1= self.input_dir+'/'+self.cUser+'_'+self.cGrad+'_'+self.cCelula+'_'+self.cZ1+'.csv'

            dict1 ={}
            dict2 = {}
            dictUpdate = {}
            listUdp = []
            listd2 = []
            listd1 = []
            listKey=[]

            with open(self.csv2, newline='') as t2 , open(self.csv1, newline='') as t1:
                f1 = csv.reader(t1,delimiter=',')
                f2 = csv.reader(t2,delimiter=',')

                for line in f2:
                    if line[0] == 'Description':
                        continue
                    if line[0] == 'Summary':
                        continue
                    if line[0] == 'Total:':
                        continue
                    if line[0]=='':
                        break
                    #print(line)
                    dict2.update({line[0]:int(line[1])})

                for line in f1:
                    if line[0] == 'Description':
                        continue
                    if line[0] == 'Summary':
                        continue
                    if line[0] == 'Total:':
                        continue
                    if line[0]=='':
                        break
                    #print(line)
                    dict1.update({line[0]:int(line[1])})

            for k, v in dict2.items():
                listd2.append(v)

            dictUpdate = {x: dict2[x] - dict1[x] for x in dict2 if x in dict1}

            for k,v in dict2.items():
                if k not in dictUpdate.keys():
                    dictUpdate.update({k:v})


            for k,v in dictUpdate.items():
                listUdp.append(v)
                listKey.append(k)

            dict11 = dict1.copy()

            for k,v in dict2.items():
                if k not in dict1.keys():
                    dict11.update({k:'inexistent'})

            for k,v in dict11.items():
                listd1.append(v)

            self.listOfTuple = list(zip(listKey,listd2,listd1,listUdp))


            for i in reversed(range(self.tableWidget.rowCount())):
                self.tableWidget.removeRow(i)




            for rows in self.listOfTuple:
                row = self.tableWidget.rowCount()
                self.tableWidget.insertRow(row)
                self.tableWidget.setColumnCount(len(rows))
                for col, info in enumerate(rows):
                    #print(type(info))
                    item = QTableWidgetItem(str(info))
                    self.tableWidget.setItem(row,col,item)



            #self.tableWidget.setHorizontalHeaderLabels(csv_headings) #seteaza header primul rand din tabel
            self.tableWidget.setHorizontalHeaderLabels(['Denumire Element',self.cZ2,self.cZ1,'Diferente','Modified','Type'])
            #self.tableWidget.horizontalHeader().setStyleSheet("QHeaderView { font-size:  12pt};")
            self.tableWidget.horizontalHeader().setStyleSheet("::section {background-color : lightGray;font-size:12pt;}")
            self.tableWidget.setColumnWidth(0,280)
            self.tableWidget.setColumnWidth(1,80)
            self.tableWidget.setColumnWidth(2,80)
            #self.tableWidget.update()

        except:
            msg = QMessageBox()
            msg.setText("Nu ai selectat calea catre fisierele .CSV")
            msg.setWindowTitle("Selecteaza folderul!")
            msg.setWindowIcon(QIcon('cross-script.png'))
            msg.setIcon(QMessageBox.Information)
            msg.setStyleSheet("background-color: brown; color: white") # la fel ca orice buton
#            msg.setStyleSheet("text-color: rgb(255, 255, 255);") #asta e culoare din jurul inconului INFO
            msg.exec_()



##    def clearTable(self):
##        for i in self.listOfTuple:
##            print(i[0])







app = QApplication(sys.argv)
window = Ui()
window.show()
app.exec_()