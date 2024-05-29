import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QStackedLayout,
                             QLineEdit, QScrollArea)
from ScheduleReader.reader import ScheduleReader


class Search_Employee_Window(QWidget):
    def __init__(self):
        super().__init__()
        sr = ScheduleReader()
        sr.add_employees()
        self.initUI()

    def initUI(self):
        self.label = QLabel("Search By Employee", self)
        self.output_label = QLabel("Output will be shown here", self)  # Label to display output
        self.textbox = QLineEdit(self)
        self.enter_button = QPushButton('Enter', self)
        self.clear_button = QPushButton('Clear', self)

        # Connect the buttons to their respective functions
        self.enter_button.clicked.connect(self.displayText)
        self.clear_button.clicked.connect(self.clearText)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.textbox)
        layout.addWidget(self.enter_button)
        layout.addWidget(self.clear_button)
        layout.addWidget(self.output_label)  # Add the output label to the layout
        self.setLayout(layout)

    def displayText(self):
        # Get the text from the textbox and display it in the output label
        entered_text = self.textbox.text()
        sr = ScheduleReader()
        sr.add_employees()
        self.textbox.clear()
        self.output_label.setText(str(sr.get_shifts_by_employee(entered_text)))

    def clearText(self):
        # Clear the textbox and the output label when Clear is clicked
        self.textbox.clear()
        self.output_label.clear()



class Search_Position_Window(QWidget):
    def __init__(self):
        super().__init__()

        self.label = QLabel("Search By Position", self)
        self.output_label = QLabel("Output will be shown here", self)  # Label to display output
        self.output_label.setWordWrap(True)  # Enable word wrap

        # Create a scroll area for the output label
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.output_label)

        self.textbox = QLineEdit(self)
        self.enter_button = QPushButton('Enter', self)
        self.clear_button = QPushButton('Clear', self)

        # Connect the buttons to their respective functions
        self.enter_button.clicked.connect(self.displayText)
        self.clear_button.clicked.connect(self.clearText)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.textbox)
        layout.addWidget(self.enter_button)
        layout.addWidget(self.clear_button)
        layout.addWidget(self.scroll_area)  # Add the scroll area to the layout instead of the label
        self.setLayout(layout)

    def displayText(self):
        # Get the text from the textbox and display it in the output label
        entered_text = self.textbox.text()
        sr = ScheduleReader()
        sr.add_employees()
        self.textbox.clear()
        employees = sr.get_shifts_by_position(entered_text)
        output_string = ""
        for employee in employees:
            output_string += str(employee) + "\n"  # Add a newline character for each employee
        self.output_label.setText(output_string)

    def clearText(self):
        # Clear the textbox and the output label when Clear is clicked
        self.textbox.clear()
        self.output_label.clear()

class All_Employee_Window(QWidget):
    def __init__(self):
        super().__init__()
        sr = ScheduleReader()
        sr.add_employees()
        self.label = QLabel("Display All Employees")
        self.output_label = QLabel("Output will be shown here", self)  # Label to display output
        self.output_label.setWordWrap(True)  # Enable word wrap

        # Create a scroll area for the output label
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.output_label)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.scroll_area)  # Add the scroll area to the layout instead of the label
        self.setLayout(layout)

        self.displayText()

    def displayText(self):
        # Get the text from the textbox and display it in the output label
        sr = ScheduleReader()
        sr.add_employees()
        employees = sr.get_all_employees()
        output_string = ""
        for employee in employees:
            output_string += str(employee) + "\n"  # Add a newline character for each employee
        self.output_label.setText(output_string)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create a stacked layout
        self.stacked_layout = QStackedLayout()

        # Create instances of the screens
        self.screen1 = Search_Employee_Window()
        self.screen2 = Search_Position_Window()
        self.screen3 = All_Employee_Window()

        # Add screens to the stacked layout
        self.stacked_layout.addWidget(self.screen1)
        self.stacked_layout.addWidget(self.screen2)
        self.stacked_layout.addWidget(self.screen3)

        # Set the central widget to the stacked layout
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.stacked_layout)
        self.setCentralWidget(self.central_widget)

        # Create buttons to switch screens
        self.button1 = QPushButton("Shifts By Employee Name")
        self.button2 = QPushButton("Shifts by Employee Position")
        self.button3 = QPushButton("Show all Employee Shifts")

        # Connect buttons to show the corresponding screens
        self.button1.clicked.connect(lambda: self.stacked_layout.setCurrentWidget(self.screen1))
        self.button2.clicked.connect(lambda: self.stacked_layout.setCurrentWidget(self.screen2))
        self.button3.clicked.connect(lambda: self.stacked_layout.setCurrentWidget(self.screen3))

        # Create a main layout
        self.main_layout = QVBoxLayout()

        # Add the stacked layout widget to the main layout
        self.main_layout.addWidget(self.central_widget)

        # Add buttons to the main layout
        self.main_layout.addWidget(self.button1)
        self.main_layout.addWidget(self.button2)
        self.main_layout.addWidget(self.button3)

        # Create a container widget and set the main layout
        self.container_widget = QWidget()
        self.container_widget.setLayout(self.main_layout)

        # Set the container widget as the central widget of the window
        self.setCentralWidget(self.container_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
