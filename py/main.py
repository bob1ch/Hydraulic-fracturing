import sys
from PyQt5.QtWidgets import QApplication,QWidget,QPlainTextEdit,QMessageBox,QLineEdit
from PyQt5.QtWidgets import QScrollArea,QVBoxLayout, QAbstractItemView, QListWidget,\
                        QListWidgetItem, QPushButton, QFileDialog,QDialog,QMainWindow
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic,QtGui,QtCore
from PyQt5.QtCore import Qt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import numpy as np
import pickle


from matplotlib.backends.backend_qt5agg import FigureCanvas,\
                     NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from engine import Engine; #custom file for computations

uifile_0 = os.path.join("..","ui","start_window.ui"); # Enter file here.
uifile_1 = os.path.join("..","ui","About.ui"); # Enter file here.
uifile_2 = os.path.join("..","ui","Help.ui"); # Enter file here.
uifile_3 = os.path.join("..","ui","input_window.ui"); # Enter file here.
uifile_4 = os.path.join("..","ui","saaa.ui"); # Enter file here.


#styles
css_filepath = os.path.join("..","ui","css","css.css");

form_0, base_0 = uic.loadUiType(uifile_0)
form_1, base_1 = uic.loadUiType(uifile_1)
form_2, base_2 = uic.loadUiType(uifile_2)
form_3, base_3 = uic.loadUiType(uifile_3)
form_4, base_4 = uic.loadUiType(uifile_4)

cached_data_fn='config.bak';


class CssMainWindow(QMainWindow):
    def __init__(self,css_filepath):
        super().__init__();
        ##http://doc.crossplatform.ru/qt/4.5.0/stylesheet-reference.html         
        #set stylesheet
        f = open(css_filepath, 'r');
        css_string = f.read();
        f.closed;     
        self.setStyleSheet(css_string); 

class CssDialog(QDialog):
    def __init__(self,css2_filepath):
        super().__init__();
        ##http://doc.crossplatform.ru/qt/4.5.0/stylesheet-reference.html         
        #set stylesheet
        f = open(css_filepath, 'r');
        css_string = f.read();
        f.closed;     
        self.setStyleSheet(css_string);


class Start(CssMainWindow, form_0):
    def __init__(self,css_filepath):
        super().__init__(css_filepath);
        self.setupUi(self)
        self.css=css_filepath;
        #window properties of the main class
        self.inputWin=[];
        self.outputWin=[];

        #test
        print('init completed');
        
        #setup button events
        self.btnInput.clicked.connect(self.openInputWindow)
        self.btnAbout.clicked.connect(self.openAboutWindow)
        self.btnHelp.clicked.connect(self.openHelpWindow)
        self.btnOutput.clicked.connect(self.opensaaaWindow)

    def openInputWindow(self):
        self.inputWin=InputWin(self.css);
        self.inputWin.show();

    def openAboutWindow(self):
        self.aboutWin = AboutWin(self.css);
        self.aboutWin.show();

    def openHelpWindow(self):
        self.helpWin = HelpWin(self.css);
        self.helpWin.show();
    def opensaaaWindow(self):
        self.saaaWin = SaaaWin(self.css);
        self.saaaWin.show();




class AboutWin(CssDialog, form_1):
    def __init__(self,css_filepath):
        super().__init__(css_filepath);
        self.setupUi(self)
        self.btnOk.clicked.connect(self.back_startWindow)
    def back_startWindow(self):
        self.hide()

class HelpWin(CssDialog, form_2):
    def __init__(self,css_filepath):
        super().__init__(css_filepath);
        self.setupUi(self)
        self.btnOk.clicked.connect(self.back_startWindow)
    def back_startWindow(self):
        self.hide()


class InputWin(CssDialog, form_3):
    def __init__(self,css_filepath):
        super().__init__(css_filepath);
        self.setupUi(self);
        
        self.btnOk.clicked.connect(self.solv)
        
        #loading cached data 
        if (os.path.exists(cached_data_fn)):
            self.initUI();    
            
                   
            
    def initUI(self):
        
        buttonReply = QMessageBox.question(self, 'Configuration was found..', "Load previous config?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            self.load_config();
        else:
            print('Do not load...');

        self.show()
        
    def load_config(self):
        f = open(cached_data_fn,'rb')  
        param_dictionary=pickle.load(f);
        
        for key in param_dictionary:
            #command='self.'+key+'.setText('+'\"'+str(param_dictionary[key])+'\"'+')';
            command='self.%s.setText(\"%s\")'%(key,param_dictionary[key]);
            print(command);
            eval(command);

    def solv(self):
       
        #QMessageBox.about(self, "Title", ("Value="+self.varDepth.text()))
        
        """
        f = open('cache','rb')  
        param_dictionary_temp=pickle.load(f);
        print('TEST_ME', param_dictionary)
        """
        param_dictionary={};
        
        for mstr in self.__dict__:
            try:
                print(mstr);
                #print(type(eval('self.'+mstr)));
                if type(eval('self.'+mstr)) == QLineEdit:
                    print('Object is line edit text field');
                    param_dictionary.update({mstr:eval('self.'+mstr+'.text()')})
            except:
                print('something went wrong :(');
        
        for key in [*param_dictionary]:
            try:
               param_dictionary[key]= float(param_dictionary[key]);
            except:
               QMessageBox.about(self,'',('error in '+key));
               return;
        
        eng = Engine();
        eng.compute2(param_dictionary); #передача параметров в движОк
        
        #сохранялка
        f = open(cached_data_fn,'wb')                            
        pickle.dump(param_dictionary,f)
        print('OK')
        
        print(param_dictionary);
        self.close();
        """
        msg = QMessageBox();
        msg.setWindowTitle("FYI!")
        msg.setText("Value="+self.varDepth.text())
        msg.setDefaultButton(QMessageBox.Ok)
        msg.exec_();
        """
        print(eng.ef)


# Ползунки и крутилка
class SaaaWin(CssDialog, form_4):
    def __init__(self, css_filepath):
        super().__init__(css_filepath);
        self.setupUi(self)
        self.sld1.setRange(0,50) #Устанавливаем минимальное и максимальное значение для ползунка 1
        self.sld2.setRange(0,50) #Устанавливаем минимальное и максимальное значение для ползунка 2
        self.sld3.setRange(0,50) #Устанавливаем минимальное и максимальное значение для ползунка 3
        self.dl1.setRange(-45,45) #Устанавливаем минимальное и максимальное значение для крутилки
        self.sld1.valueChanged.connect(self.Reset) #Событие
        self.sld2.valueChanged.connect(self.Reset) #Событие
        self.sld3.valueChanged.connect(self.Reset) #Событие
        self.dl1.valueChanged.connect(self.Reset) #Событие
    def Reset(self):
        f=self.dl1.value() #Значение крутилки
        self.lb4.setText(str('Угол: ' + str(f))) #Изменение текста
        g = self.sld1.value() #Значение ползунка 1
        self.lb1.setText(str('Глубина: ' + str(g))) #Изменение текста
        h = self.sld2.value() #Значение ползунка 2
        self.lb2.setText(str('Ширина: ' + str(h))) #Изменение текста
        d = self.sld3.value() #Значение ползунка 3
        self.lb3.setText(str('Длина: ' + str(d))) #Изменение текста
        W = d*h*g + 0.5*h*d**2 * np.tan(f/180*3.14)
        self.lbl.setText(str('Объем: ' + str(W))) #Изменение текста


        '''Depth = int(self.varDepth.text())
        varThickness = int(self.varThickness.text())
        varPoisson = int(self.varPoisson.text())
        varPermeability = int(self.varPermeability.text())
        varYoung = int(self.varYoung.text())
        S = Depth + varYoung + varThickness + varPoisson + varPermeability
        print(S)'''
        #the way to initialize computations in the engine

        

'''class InputWin(CssDialog, form_3):
    def __init__(self,css_filepath):
        super().__init__(css_filepath);        self.setupUi(self)
        
        #the way to initialize computations in the engine
        eng.compute(); 
        




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
        
        #print(css_string);
        
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
            
        self.tableView.setModel(model);'''






if __name__ == '__main__':
    pass;
    app = QApplication(sys.argv)
    ex = Start(css_filepath)
    ex.show()
    sys.exit(app.exec_())




