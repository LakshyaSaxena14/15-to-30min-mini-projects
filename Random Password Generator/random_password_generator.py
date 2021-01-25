from PySide2.QtWidgets import *
import sys
import random
import pyperclip

characters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
              't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
              'O', 'P', 'Q', 'R', 'S', 'T',
              'U', 'V', 'W', 'X', 'Y', 'Z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '`', '~', '!', '@', '#',
              '$', '%', '^', '&', '*', '(', ')', '-', '_', '[', ']', '{', '}', ';',
              ':', '"', '\'', '<', ',', '>', '>', '/', '?', '|', '\\']

length = random.choice(range(13, 20))

password = "".join(random.sample(characters, length))
print(password)
pyperclip.copy(password)


class RandomPasswordGenerator(QMainWindow):
    def __init__(self):
        super(RandomPasswordGenerator, self).__init__()

        self.resize(603, 279)
        self.setWindowTitle("Random Password Generator")

        self.setStyleSheet("background-color: rgb(50, 50, 50);\n"
                           "color: rgb(255, 255, 255);\n"
                           "border-color: rgb(255, 255, 255);\n"
                           "font: 12pt Ubuntu;")

        self.centralwidget = QWidget(self)
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(10, 0, 601, 61)
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.password_label = QLabel(self.verticalLayoutWidget)
        self.password_label.setText("Your Random Password is: ")

        self.verticalLayout.addWidget(self.password_label)

        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(30, 90, 491, 131)
        self.horizontalLayout_3 = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)

        self.label = QLabel(self.horizontalLayoutWidget)
        self.label.setText(f"{password}\n\n\n\n Pro Tip: this password has been copied to your clipboard.")
        self.label.adjustSize()

        self.horizontalLayout_3.addWidget(self.label)

        self.setCentralWidget(self.centralwidget)

        self.menubar = QMenuBar(self)
        self.menubar.setGeometry(0, 0, 603, 22)
        self.setMenuBar(self.menubar)

        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RandomPasswordGenerator()
    window.show()
    sys.exit(app.exec_())
