import sys

from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QStackedLayout,
                             QLineEdit, QScrollArea, QSpacerItem, QSizePolicy, QComboBox, QDesktopWidget)
from PyQt5.QtCore import Qt, QSize
from ScheduleReader.reader import ScheduleReader

TEXTBOX_STYLE = "QLineEdit { border: 1px solid #023047; }"
SCROLL_AREA_STYLE = "QScrollArea { border: none; }"


# Updated color scheme
BACKGROUND_COLOR = '#8ecae6'  # Light blue background
BUTTON_COLOR = '#023047'      # Dark blue buttons
TEXT_COLOR = '#ff8c00'        # Orange text
HOVER_COLOR = '#219ebc'       # Blue hover effect

# Define the desired font size
FONT_SIZE = '20pt'

# Updated button style with font size
BUTTON_STYLE = f"QPushButton {{ background-color: {BUTTON_COLOR}; color: {TEXT_COLOR}; font-size: {FONT_SIZE}; }}"
BUTTON_HOVER_STYLE = f"QPushButton:hover {{ background-color: {HOVER_COLOR}; }}"
LABEL_STYLE = "QLabel { color: #023047; font-size: 50px; }"

from screeninfo import get_monitors

# Get screen size
monitor = get_monitors()[0]
screen_width = monitor.width
screen_height = monitor.height

# Calculate button size based on screen size
button_width = int(screen_width * 0.5)  # 50% of screen width
button_height = int(screen_height * 0.1)  # 10% of screen height
button_size = QSize(button_width, button_height)

other_button_width = int(screen_width * 0.1)  # 50% of screen width
other_button_height = int(screen_height * 0.05)  # 10% of screen height
other_button_size = QSize(other_button_width, other_button_height)

scroll_width = int(screen_width * 0.5)
scroll_height = int(screen_height * 0.1)
class Initial_Screen(QMainWindow):
    def __init__(self, stacked_layout):
        super().__init__()
        self.setWindowTitle('Schedule Reader')
        self.stacked_layout = stacked_layout
        self.initUI()

    def initUI(self):
        self.setStyleSheet(f"background-color: {BACKGROUND_COLOR};")
        self.button1 = QPushButton("Shifts By Employee Name", self)
        self.button2 = QPushButton("Shifts by Employee Position", self)
        self.button3 = QPushButton("Show all Employee Shifts", self)

        # Set button styles
        self.button1.setStyleSheet(BUTTON_STYLE)
        self.button2.setStyleSheet(BUTTON_STYLE)
        self.button3.setStyleSheet(BUTTON_STYLE)

        # Set button icons
        self.button1.setIcon(QIcon('./images/employee.png'))
        self.button2.setIcon(QIcon('./images/Position.jpg'))
        self.button3.setIcon(QIcon('./images/All.jpg'))

        # Set button tooltips
        self.button1.setToolTip('Enter an employee\'s name to view their shifts.')
        self.button2.setToolTip('Select a position to see corresponding employee shifts.')
        self.button3.setToolTip('Click here to display all employee shifts in the system.')

        self.button1.clicked.connect(lambda: self.stacked_layout.setCurrentIndex(1))
        self.button2.clicked.connect(lambda: self.stacked_layout.setCurrentIndex(2))
        self.button3.clicked.connect(lambda: self.stacked_layout.setCurrentIndex(3))

        # Set button size
        self.button1.setFixedSize(button_size)
        self.button2.setFixedSize(button_size)
        self.button3.setFixedSize(button_size)

        # Add image label
        image_label = QLabel(self)
        image_label.setPixmap(QPixmap('./images/stonewall-golf-color-logo.png'))  # Replace with your image path
        image_label.setAlignment(Qt.AlignCenter)

        # Adjust layout to include image
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.addWidget(image_label, alignment=Qt.AlignCenter)  # Add image label to layout
        layout.addWidget(self.button1, alignment=Qt.AlignCenter)
        layout.addWidget(self.button2, alignment=Qt.AlignCenter)
        layout.addWidget(self.button3, alignment=Qt.AlignCenter)

        # Add description label
        description_label = QLabel("Schedule Reader: Easily view employee shifts at Stonewall Golf Club.")
        description_label.setStyleSheet(LABEL_STYLE)
        layout.addWidget(description_label, alignment=Qt.AlignCenter)

        # Add spacers for better layout
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

class BaseScreen(QWidget):
    def __init__(self, stacked_layout, schedule_reader):
        super().__init__()
        self.sr = schedule_reader
        self.stacked_layout = stacked_layout


from PyQt5.QtCore import pyqtSignal


class ResizableLabel(QLabel):
    # Define a custom signal
    textChanged = pyqtSignal(str)

    def __init__(self, parent=None):
        super(ResizableLabel, self).__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setAlignment(Qt.AlignCenter)

    def setText(self, text):
        # Emit the textChanged signal whenever the text is set
        super(ResizableLabel, self).setText(text)
        self.textChanged.emit(text)

    def sizeHint(self):
        # Calculate the size hint based on the content
        # Set a reasonable maximum width for the label
        return QSize(scroll_width, scroll_height)


class Search_Employee_Screen(BaseScreen):
    def __init__(self, stacked_layout, schedule_reader):
        super().__init__(stacked_layout, schedule_reader)

        # Styling constants
        SEARCH_BAR_HEIGHT = 60
        BUTTON_WIDTH = 100
        FONT_SIZE = 50

        # Set the style for the search bar, buttons, and scroll area
        self.setStyleSheet("""
                            QLineEdit {
                                height: %dpx;
                                font-size: %dpx;
                            }
                            QPushButton {
                                width: %dpx;
                                font-size: %dpx;
                            }
                            QLabel {
                                font-size: %dpx;
                            }
                        """ % (SEARCH_BAR_HEIGHT, FONT_SIZE, BUTTON_WIDTH, FONT_SIZE, FONT_SIZE))
        image_label = QLabel(self)
        image_label.setPixmap(QPixmap('./images/stonewall-golf-color-logo.png'))  # Replace with your image path
        image_label.setAlignment(Qt.AlignCenter)
        self.label = QLabel("Search By Employee", self)
        self.label.setStyleSheet(LABEL_STYLE)
        self.output_label = QLabel("", self)
        self.output_label = ResizableLabel(self)
        self.output_label.setWordWrap(True)
        self.output_label.setStyleSheet(LABEL_STYLE)

        # Connect the custom signal to the slot
        self.output_label.textChanged.connect(self.updateScrollAreaSize)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.output_label)

        self.textbox = QLineEdit(self)
        self.textbox.setStyleSheet(TEXTBOX_STYLE)
        self.enter_button = QPushButton('Enter', self)
        self.enter_button.setStyleSheet(BUTTON_STYLE)
        self.enter_button.setFixedSize(other_button_size)
        self.clear_button = QPushButton('Clear', self)
        self.clear_button.setStyleSheet(BUTTON_STYLE)
        self.clear_button.setFixedSize(other_button_size)

        self.back_button = QPushButton('Exit', self)
        self.back_button.setStyleSheet(BUTTON_STYLE)
        self.back_button.setFixedSize(150, 75)  # Width: 150 pixels, Height: 50 pixels
        self.back_button.clicked.connect(lambda: self.stacked_layout.setCurrentIndex(0))

        self.enter_button.clicked.connect(self.displayText)
        self.clear_button.clicked.connect(self.clearText)

        vertical_spacer_top = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        vertical_spacer_bottom = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        # Adjust layout spacing and margins
        layout = QVBoxLayout()
        layout.addWidget(image_label, alignment=Qt.AlignCenter)  # Add image label to layout
        layout.setContentsMargins(20, 20, 20, 20)  # Adjust margins as needed
        layout.setSpacing(10)  # Reduce spacing to bring elements closer

        # Add widgets and spacers to the layout
        layout.addWidget(self.label, alignment=Qt.AlignCenter)
        layout.addWidget(self.textbox, alignment=Qt.AlignCenter)
        layout.addWidget(self.enter_button, alignment=Qt.AlignCenter)
        layout.addWidget(self.clear_button, alignment=Qt.AlignCenter)
        layout.addItem(vertical_spacer_top)  # Add spacer before the scroll area
        layout.addWidget(self.scroll_area, alignment=Qt.AlignCenter)
        layout.addItem(vertical_spacer_bottom)  # Add spacer after the scroll area

        self.setLayout(layout)

    def updateScrollAreaSize(self):
        # Update the size policy based on the content size
        content_size = self.output_label.sizeHint()
        self.scroll_area.setMinimumSize(content_size.width(), content_size.height())

    def displayText(self):
        entered_text = self.textbox.text()
        self.textbox.clear()
        try:
            shifts_info = self.sr.get_shifts_by_employee(entered_text)
            self.output_label.setText(str(shifts_info))
        except Exception as e:
            self.output_label.setText("Error: " + str(e))

    def clearText(self):
        self.textbox.clear()
        self.output_label.clear()


class Search_Position_Screen(BaseScreen):
    def __init__(self, stacked_layout, schedule_reader):
        super().__init__(stacked_layout, schedule_reader)
        # Styling constants
        SEARCH_BAR_HEIGHT = 60
        BUTTON_WIDTH = 100
        FONT_SIZE = 50

        # Set the style for the search bar, buttons, and scroll area
        self.setStyleSheet("""
                                    QLineEdit {
                                        height: %dpx;
                                        font-size: %dpx;
                                    }
                                    QPushButton {
                                        width: %dpx;
                                        font-size: %dpx;
                                    }
                                    QLabel {
                                        font-size: %dpx;
                                    }
                                """ % (SEARCH_BAR_HEIGHT, FONT_SIZE, BUTTON_WIDTH, FONT_SIZE, FONT_SIZE))

        image_label = QLabel(self)
        image_label.setPixmap(QPixmap('./images/stonewall-golf-color-logo.png'))  # Replace with your image path
        image_label.setAlignment(Qt.AlignCenter)

        self.label = QLabel("Search By Position", self)
        self.label.setStyleSheet(LABEL_STYLE)
        self.output_label = QLabel("", self)
        self.output_label = ResizableLabel(self)
        self.output_label.setWordWrap(True)
        self.output_label.setStyleSheet(LABEL_STYLE)

        # Connect the custom signal to the slot
        self.output_label.textChanged.connect(self.updateScrollAreaSize)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.output_label)

        self.combo_box = QComboBox(self)
        self.combo_box.setStyleSheet("QComboBox { font-size: 16pt; }" + TEXTBOX_STYLE)
        # Add the four different choices to the combo box
        self.combo_box.addItems(["GOLF SHOP", "STARTERS/MARSHALS", "CART ATTENDANTS", "BEV CART ATTENDANTS"])

        self.combo_box.setFixedSize(other_button_size)

        self.enter_button = QPushButton('Enter', self)
        self.enter_button.setStyleSheet(BUTTON_STYLE)
        self.clear_button = QPushButton('Clear', self)
        self.clear_button.setStyleSheet(BUTTON_STYLE)

        self.back_button = QPushButton('Exit', self)
        self.back_button.setStyleSheet(BUTTON_STYLE)
        self.back_button.setFixedSize(150, 75)  # Width: 150 pixels, Height: 50 pixels
        self.back_button.clicked.connect(lambda: self.stacked_layout.setCurrentIndex(0))

        self.enter_button.clicked.connect(self.displayText)
        self.clear_button.clicked.connect(self.clearText)

        vertical_spacer_top = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        vertical_spacer_bottom = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        layout = QVBoxLayout()
        layout.addWidget(image_label, alignment=Qt.AlignCenter)  # Add image label to layout
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # Add widgets and spacers to the layout
        layout.addWidget(self.label, alignment=Qt.AlignCenter)
        layout.addWidget(self.combo_box, alignment=Qt.AlignCenter)  # Add the combo box instead of the textbox
        layout.addWidget(self.enter_button, alignment=Qt.AlignCenter)
        layout.addWidget(self.clear_button, alignment=Qt.AlignCenter)
        layout.addItem(vertical_spacer_top)
        layout.addWidget(self.scroll_area, alignment=Qt.AlignCenter)
        layout.addItem(vertical_spacer_bottom)

        self.setLayout(layout)
    def updateScrollAreaSize(self):
        # Update the size policy based on the content size
        content_size = self.output_label.sizeHint()
        self.scroll_area.setMinimumSize(content_size.width(), content_size.height())

    def displayText(self):
        # Get the text from the textbox and display it in the output label
        selected_text = self.combo_box.currentText()
        employees = self.sr.get_shifts_by_position(selected_text)
        output_string = ""
        for employee in employees:
            output_string += str(employee) + "\n"  # Add a newline character for each employee
        self.output_label.setText(output_string)

    def clearText(self):
        # Clear the textbox and the output label when Clear is clicked
        self.textbox.clear()
        self.output_label.clear()


class All_Employee_Screen(BaseScreen):
    def __init__(self, stacked_layout, schedule_reader):
        super().__init__(stacked_layout, schedule_reader)
        # Styling constants
        SEARCH_BAR_HEIGHT = 60
        BUTTON_WIDTH = 100
        FONT_SIZE = 50

        # Set the style for the search bar, buttons, and scroll area
        self.setStyleSheet("""
                                            QLineEdit {
                                                height: %dpx;
                                                font-size: %dpx;
                                            }
                                            QPushButton {
                                                width: %dpx;
                                                font-size: %dpx;
                                            }
                                            QLabel {
                                                font-size: %dpx;
                                            }
                                        """ % (SEARCH_BAR_HEIGHT, FONT_SIZE, BUTTON_WIDTH, FONT_SIZE, FONT_SIZE))

        image_label = QLabel(self)
        image_label.setPixmap(QPixmap('./images/stonewall-golf-color-logo.png'))  # Replace with your image path
        image_label.setAlignment(Qt.AlignCenter)

        self.label = QLabel("Show All Employees", self)
        self.output_label = QLabel("", self)
        self.output_label = ResizableLabel(self)
        self.output_label.setWordWrap(True)
        self.output_label.setStyleSheet(LABEL_STYLE)

        # Connect the custom signal to the slot
        self.output_label.textChanged.connect(self.updateScrollAreaSize)

        self.back_button = QPushButton('Exit', self)
        self.back_button.setStyleSheet(BUTTON_STYLE)
        self.back_button.setFixedSize(150, 75)  # Width: 150 pixels, Height: 50 pixels
        self.back_button.clicked.connect(lambda: self.stacked_layout.setCurrentIndex(0))

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.output_label)

        vertical_spacer_top = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        vertical_spacer_bottom = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        # Adjust layout spacing and margins
        layout = QVBoxLayout()
        layout.addWidget(image_label, alignment=Qt.AlignCenter)  # Add image label to layout
        layout.setContentsMargins(20, 20, 20, 20)  # Adjust margins as needed
        layout.setSpacing(10)  # Reduce spacing to bring elements closer

        # Add widgets and spacers to the layout
        layout.addWidget(self.label, alignment=Qt.AlignCenter)
        layout.addItem(vertical_spacer_top)  # Add spacer before the scroll area
        layout.addWidget(self.scroll_area, alignment=Qt.AlignCenter)
        layout.addItem(vertical_spacer_bottom)  # Add spacer after the scroll area

        self.setLayout(layout)

        self.displayText()

    def updateScrollAreaSize(self):
        # Update the size policy based on the content size
        content_size = self.output_label.sizeHint()
        self.scroll_area.setMinimumSize(content_size.width(), content_size.height())

    def displayText(self):
        # Get the text from the textbox and display it in the output label
        employees = self.sr.get_all_employees()
        output_string = ""
        for employee in employees:
            output_string += str(employee) + "\n"  # Add a newline character for each employee
        self.output_label.setText(output_string)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.sr = ScheduleReader()
        self.sr.add_employees()

        self.stacked_layout = QStackedLayout()

        self.setStyleSheet(f"background-color: {BACKGROUND_COLOR};")

        self.screen0 = Initial_Screen(self.stacked_layout)
        self.screen1 = Search_Employee_Screen(self.stacked_layout, self.sr)
        self.screen2 = Search_Position_Screen(self.stacked_layout, self.sr)
        self.screen3 = All_Employee_Screen(self.stacked_layout, self.sr)

        self.stacked_layout.addWidget(self.screen0)
        self.stacked_layout.addWidget(self.screen1)
        self.stacked_layout.addWidget(self.screen2)
        self.stacked_layout.addWidget(self.screen3)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.stacked_layout)
        self.setCentralWidget(self.central_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
