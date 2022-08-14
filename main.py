
import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPalette, QColor



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
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        
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


        data_row = data.iloc[self.selected_row,:].values
        print(data_row)
        print(self.selected_row)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()