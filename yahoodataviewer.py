import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import yahoofinance as yf

class YahooFetch(QMainWindow):

    def __init__(self, parent=None):

        QMainWindow.__init__(self, parent)

        self.setWindowTitle('Yahoo! Stock Data')
        self.create_widgets()
        self.setup_layouts()
        self.setCentralWidget(self.figure_widget)

    def update_fig(self):

        try:
            data = yf.get_historic_dataframe(unicode(self.ticker_box.text()),
            unicode(self.start_date_box.text()),
            unicode(self.end_date_box.text()))
        except ValueError as e:
            print e.message
            return

        self.axes.clear()

        self.axes.plot(data['Date'].values,data['Close'].values)

        self.fig.autofmt_xdate()
        
        self.canvas.draw()

    def create_widgets(self):

        self.create_figure()

        self.load_button = QPushButton("&Load")
        self.connect(self.load_button, SIGNAL('clicked()'), self.update_fig)

        self.create_ticker_box()

        self.create_date_boxes()

    def setup_layouts(self):

        hbox = QHBoxLayout()

        for w in [  self.load_button, self.ticker_box_label, self.ticker_box,
                    self.start_date_label, self.start_date_box,
                    self.end_date_label, self.end_date_box]:
            hbox.addWidget(w)
            hbox.setAlignment(w, Qt.AlignVCenter)

        vbox = QVBoxLayout()
        vbox.addWidget(self.canvas)
        vbox.addLayout(hbox)

        self.figure_widget.setLayout(vbox)

    def create_figure(self):

        self.figure_widget = QWidget()

        self.dpi = 200
        self.fig = Figure(figsize=(4, 4),dpi=self.dpi)

        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.figure_widget)

        self.axes = self.fig.add_subplot(111)
        self.fig.autofmt_xdate()

    def create_ticker_box(self):

        self.ticker_box_label = QLabel('Ticker Symbol:')
        self.ticker_box = QLineEdit()
        regexp_ticker = QRegExp('^[A-Z]{0,6}$')
        validator_ticker = QRegExpValidator(regexp_ticker)
        self.ticker_box.setValidator(validator_ticker)

    def create_date_boxes(self):

        self.start_date_label = QLabel('Start Date (mm/dd/yyyy):')
        self.end_date_label = QLabel('End Date (mm/dd/yyyy):')

        self.start_date_box = QLineEdit()
        self.end_date_box = QLineEdit()
        regexp_date = QRegExp('^[0-9]{1,2}/[0-9]{1,2}/[0-9]{4}$')
        validator_date = QRegExpValidator(regexp_date)
        self.start_date_box.setValidator(validator_date)
        self.end_date_box.setValidator(validator_date)

if __name__ == "__main__":

    app = QApplication(sys.argv)
    form = YahooFetch()
    form.show()
    app.exec_()
