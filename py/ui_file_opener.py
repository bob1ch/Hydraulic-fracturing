import sys
from PyQt5.QtWidgets import QApplication,QWidget,QPlainTextEdit
from PyQt5.QtWidgets import QScrollArea,QVBoxLayout, QAbstractItemView, QListWidget,QListWidgetItem, QPushButton, QFileDialog,QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic,QtGui,QtCore
from PyQt5.QtCore import Qt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

from matplotlib.backends.backend_qt5agg import FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


uifile_1 = os.path.join("..","ui","plot_builder_v2.ui"); # Enter file here.
uifile_2 = os.path.join("..","ui","data_window.ui"); # Enter file here.
css_filepath = os.path.join("..","ui","css","css.css");

form_1, base_1 = uic.loadUiType(uifile_1)
form_2, base_2 = uic.loadUiType(uifile_2)

class Example(base_1, form_1):
    def __init__(self,css_filepath):
        super().__init__()
        self.setupUi(self)
        #self.layout = QVBoxLayout(self)
        
        ######
        # a figure instance to plot on
        self.figure = plt.figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # set the layout
        #layout = QVBoxLayout()
        #layout.addWidget(self.toolbar)
        #layout.addWidget(self.canvas)
        self.scrollArea.setWidget(self.canvas)
        #self.setLayout(layout)
        
        #####
        ##http://doc.crossplatform.ru/qt/4.5.0/stylesheet-reference.html 
        
        #set stylesheet
        f = open(css_filepath, 'r');
        css_string = f.read();
        f.closed;     
        
        print(css_string);
        
        self.setStyleSheet(css_string);
        
        #self.setStyleSheet(css_string);
        
        self.fileOpen.clicked.connect(self.file_open_dialogue)
        self.buildBut.clicked.connect(self.build_plot)
        self.df=pd.DataFrame() #global dataframe

    def file_open_dialogue(self):
        
        fileName = QFileDialog.getOpenFileName(self,"Data files (*.csv)")
        
        #self.label.setText("Hello "+self.lineEdit.text())
        if fileName:
            print(fileName[0])
            self.filePath.setPlainText(fileName[0])
            self.df=pd.read_csv(fileName[0],sep=';')
            labels=self.df.columns
            for i in labels:
                item1 = QListWidgetItem() #need to copy theese items twice
                item1.setText(str(i))
                self.list1.addItem(item1)
            self.list1.setSelectionMode(QAbstractItemView.MultiSelection)
            self.list1.itemSelectionChanged.connect(self.on_change1)
            print(self.df)
            
        
    def build_plot(self):
        item_list=[item.text() for item in self.list1.selectedItems()]
        print(item_list)
        
        print('my_frame',self.df,'\n\n\n\n\n');
        #print(self.df(str(item_list[0])))
        idx1=item_list[0];idx2=item_list[1];
        x=self.df[idx1];
        y=self.df[idx2];
        #self._static_ax.plot(x,y)
        #plt.plot(x,y)
        #plt.show()
        ###
        self.figure.clear();

        # create an axis
        ax = self.figure.add_subplot(111);

        # discards the old graph
        # ax.hold(False) # deprecated, see above

        # plot data
        ax.plot(x,y, '*-');

        # refresh canvas
        self.canvas.draw();
        self.data_window=dataWindow(self.df);
        self.data_window.show(); 
        ###
        
    def on_change1(self):
        print("start");
        print([item.text() for item in self.list1.selectedItems()]);

#class PandasModel was taken from https://stackoverflow.com/questions/31475965/fastest-way-to-populate-qtableview-from-pandas-data-frame   
    
class dataWindow(base_2, form_2):
    def __init__(self,dataframe):
        print('new window has been created');
        super().__init__();
        self.setupUi(self);

        m,n=dataframe.values.shape;
        column_names=[colname for colname in dataframe];
        
        #set test data to QTableVIew
        model = QtGui.QStandardItemModel(m,n) #new standard item model as m,n table
        
        #populating table with data
        for row in range(0, m):
            for column in range(0, n):
               item = QtGui.QStandardItem(str(dataframe.values[row,column]));
               model.setItem(row, column, item);
               
        model.setHorizontalHeaderLabels(column_names);            
        model.setVerticalHeaderLabels([str(v) for v in dataframe.index.values.tolist()]);
            
        self.tableView.setModel(model);
        
        
            
if __name__ == '__main__':
    pass;
    app = QApplication(sys.argv)
    ex = Example(css_filepath)
    ex.show()
    sys.exit(app.exec_())
