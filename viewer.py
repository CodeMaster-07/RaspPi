from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QDialog, QLabel, QGridLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from database import fetch_all_data
import sys

class BatteryDetailDialog(QDialog):
    def __init__(self, battery_data):
        super().__init__()
        self.setWindowTitle('Battery Detail')
        self.setGeometry(300, 300, 400, 300)
        layout = QGridLayout()

        labels = [
            "Raspberry Pi", "USB Port", "State", "SOC", "Total Voltage",
            "Voltage 1", "Voltage 2", "Voltage 3", "Voltage 4", 
            "Voltage 5", "Voltage 6", "Voltage 7", "Temperature", "Upload Time"
        ]
        for i, label in enumerate(labels):
            layout.addWidget(QLabel(label), i, 0)
            layout.addWidget(QLabel(str(getattr(battery_data, label.lower().replace(' ', '_'), 'N/A'))), i, 1)
        
        self.setLayout(layout)

class TableView(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Battery Data Viewer')
        self.setGeometry(100, 100, 1200, 800)  # Adjust the window size as needed
        layout = QVBoxLayout()

        self.tableWidget = QTableWidget()
        layout.addWidget(self.tableWidget)
        self.setLayout(layout)
        self.loadData()

    def loadData(self):
        data = fetch_all_data()
        self.tableWidget.setRowCount(10)
        self.tableWidget.setColumnCount(10)  # 10 USB Ports
        self.tableWidget.setHorizontalHeaderLabels([f"usb{i+1}" for i in range(10)])
        self.tableWidget.setVerticalHeaderLabels([f"RAZ{i+1}" for i in range(10)])

        self.battery_data = {}
        
        for battery in data:
            pi_index = int(battery.raspberry_pi.replace("PI", "")) - 1
            usb_index = int(battery.usb_port.replace("USB", "")) - 1
            self.battery_data[(pi_index, usb_index)] = battery

            item = QTableWidgetItem(str(battery.soc))
            item.setTextAlignment(Qt.AlignCenter)

            if battery.state == 1:
                item.setBackground(QColor(66, 163, 57))  # Light green
            elif battery.state == 2:
                item.setBackground(QColor(255, 182, 193))  # Light red
            else:
                item.setBackground(QColor(194, 194, 58))  # Light yellow
            
            self.tableWidget.setItem(pi_index, usb_index, item)
            item.setData(Qt.UserRole, battery)
        
        # Fill empty cells with default values
        for i in range(10):
            for j in range(10):
                if (i, j) not in self.battery_data:
                    item = QTableWidgetItem("N/A")
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setBackground(QColor(211, 211, 211))  # Light gray
                    self.tableWidget.setItem(i, j, item)
        
        self.tableWidget.cellDoubleClicked.connect(self.showDetail)

    def showDetail(self, row, column):
        item = self.tableWidget.item(row, column)
        if item:
            battery_data = item.data(Qt.UserRole)
            if battery_data:
                dialog = BatteryDetailDialog(battery_data)
                dialog.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = TableView()
    viewer.show()
    sys.exit(app.exec_())
