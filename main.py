
import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *



import pandas as pd

data  = pd.read_excel('Etiquetas KG.xlsx', sheet_name='KG')
# data = pd.read_csv("C:/Users/Jesus/Documents/Diplomado/Proyecto/Datasets/TMDb/TitleToConvert.csv",nrows=10)


class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

class PandasModel(QAbstractTableModel):
    """
    Class to populate a table view with a pandas dataframe
    """
    def __init__(self, data, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self._data = data

    def rowCount(self, parent=None):
        return len(self._data.values)

    def columnCount(self, parent=None):
        return self._data.columns.size

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row()][index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None

class AddProduct(QDialog):
    def __init__(self,product_info):
        super().__init__()

        self.colclicked = 0

        self.resize(450,150)
        self.layout = QVBoxLayout()

        self.temp_product = product_info
        self.temp_product = list(map(str,self.temp_product))

        self.tableView = QTableView()
        
    
        self.model =  QStandardItemModel(0,5)
        self.model.insertRow(0,list(map(QStandardItem,self.temp_product)))
        self.model.setRowCount(1)

        

        self.model.setHeaderData(0, Qt.Horizontal,"ID")
        self.model.setHeaderData(1, Qt.Horizontal,"Descripción")
        self.model.setHeaderData(2, Qt.Horizontal,"Precio (KG)")
        self.model.setHeaderData(3, Qt.Horizontal,"Cantidad ($)")
        self.model.setHeaderData(4, Qt.Horizontal,"Cantidad (KG)")
        # self.model.setHeaderData(5, Qt.Horizontal,"Total")

        self.tableView.setModel(self.model)

        print('s')

        header = self.tableView.horizontalHeader()
        header.setSectionResizeMode(1,QHeaderView.Stretch)
        header.setSectionResizeMode(QHeaderView.Stretch)
        # header.setSectionResizeMode(0,QHeaderView.Stretch)
        # header.setSectionResizeMode(1,QHeaderView.Stretch)
        # header.setSectionResizeMode(2,QHeaderView.Stretch)
        # header.setSectionResizeMode(3,QHeaderView.Stretch)
        # header.setSectionResizeMode(4,QHeaderView.Stretch)
        
        rows= self.tableView.verticalHeader()
        rows.setSectionResizeMode(QHeaderView.Stretch)
        rows.setVisible(False)

        addbutton = QPushButton()
        addbutton.setFixedHeight(50)

        self.layout.addWidget(self.tableView)
        self.layout.addWidget(addbutton)
        self.setLayout(self.layout)

        self.tableView.clicked.connect(self.itemclicked)
        self.model.itemChanged.connect(self.Itemchanged,self.colclicked)
        addbutton.clicked.connect(self.add_co)

    def itemclicked(self,clickedIndex):
        self.colclicked = clickedIndex.column()
        # print(self.colclicked)



    def Itemchanged(self,col):
        self.data = [(str(self.model.data(self.model.index(0, colj)))) for colj in range(5)]
        # print('here')
        col = col.column()
        # print(col)
        try:
            float(self.data[3]) + 1
        except:
            self.data[3] = "0"

        try:
            float(self.data[4]) + 1
        except:
            self.data[4] = "0"

        if col == 3: # <- Fixed price
            qty= str(float(self.data[3])/float(self.temp_product[2]))
            self.data[4] = qty   
            # data_co = data
            # self.model.setData(self.model.index(0, 4), "{:.2f}".format(data[4]),0)
            self.model.setData(self.model.index(0, 4), self.data[4],0)

        if col == 4: # <- Fixed qty
            price = str(float(self.data[4])*float(self.temp_product[2]))
            self.data[3] = price
            # data_co = data
            # self.model.setData(self.model.index(0, 3), "{:.2f}".format(data[3]),0)
            self.model.setData(self.model.index(0, 3), self.data[3],0)


        self.model.setData(self.model.index(0, 0), self.temp_product[0],0)
        self.model.setData(self.model.index(0, 1), self.temp_product[1],0)
        self.model.setData(self.model.index(0, 2), self.temp_product[2],0)

        print(self.temp_product)
        print(self.data)
        # self.temp_roduct = data
        
    def add_co(self):
        self.close()
        


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1000,800)

        ## General Layout        
        general_lo = QHBoxLayout()

        
        ## Selling layout
        sell_lo = QVBoxLayout()
        

        ## Shop info
        info_lo = QHBoxLayout()
        info_lo.addWidget(Color('Blue'))
        # info_label = QLabel()
        # info_label.setText('Materias primas martinez')
        # info_label.setPalette()
        # info_lo.addWidget(info_label)


        ### Searching
        search_lo = QHBoxLayout()
        self.search = QLineEdit()
        search_lo.addWidget(self.search)



        ### Inventory
        inventory_lo = QHBoxLayout()
        view = QTableView()
        model = PandasModel(data)
        view.setModel(model)

        header = view.horizontalHeader()       
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        
        view.setSelectionBehavior(QTableView.SelectRows)
        self.selected_row=-1
        
        view.clicked.connect(self.selectedRow)

        # data_row = data.iloc[row,:]

        # print(data_row)
        # view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        inventory_lo.addWidget(view)


        #### Selling arrange
        sell_lo.addLayout(info_lo,20)
        sell_lo.addLayout(search_lo,10)
        sell_lo.addLayout(inventory_lo,70)

        


        ##
        chechout_lo = QVBoxLayout()



        ## Final arrange
        general_lo.addLayout(sell_lo,70)
        general_lo.addLayout(chechout_lo,30)


        widget = QWidget()
        widget.setLayout(general_lo)

        # Set the central widget of the Window.
        self.setCentralWidget(widget)

    def selectedRow(self, clickedIndex):
        self.selected_row = clickedIndex.row()
        self.data_row = data.iloc[self.selected_row,0:3].values

        self.add_product = AddProduct(self.data_row)
        self.add_product.exec_()
        print(self.add_product.temp_product,'asdsa')

        # print(self.data_row)
        # print(self.selected_row)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()