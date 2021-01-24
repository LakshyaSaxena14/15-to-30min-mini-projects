import time
import sys
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP as smtp
import smtplib
from email.mime.text import MIMEText as text, MIMEText
from PySide2.QtCore import QRect, QSize, QMetaObject
from PySide2.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QMenuBar, \
    QStatusBar, QApplication


class Email(QMainWindow):
    def __init__(self):
        super(Email, self).__init__()
        self.setWindowTitle("Email Sender")

        self.main_ui()

    def main_ui(self):
        self.setGeometry(QRect(40, 100, 714, 537))
        self.setFixedSize(714, 537)
        self.setStyleSheet("background-color: rgb(50, 50, 55);\n"
                           "font: 12pt \"Roboto\";\n"
                           "color: rgb(255, 255, 255);")

        self.centralwidget = QWidget(self)

        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QRect(10, 0, 641, 71))
        self.sender_email = QHBoxLayout(self.horizontalLayoutWidget)
        self.sender_email.setSpacing(10)
        self.sender_email.setContentsMargins(0, 10, 10, 10)
        self.label = QLabel(self.horizontalLayoutWidget)
        self.label_2 = QLabel(self.horizontalLayoutWidget)
        self.label_2.setText("Sender's Email Account        ")
        self.sender_email_edit = QLineEdit(self.horizontalLayoutWidget)
        self.sender_email_edit.setMinimumSize(QSize(0, 40))

        self.sender_email.addWidget(self.label)
        self.sender_email.addWidget(self.label_2)
        self.sender_email.addWidget(self.sender_email_edit)

        self.horizontalLayoutWidget_2 = QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QRect(10, 90, 641, 61))
        self.reciever_email = QHBoxLayout(self.horizontalLayoutWidget_2)
        self.reciever_email.setContentsMargins(10, 10, 10, 10)
        self.label_3 = QLabel(self.horizontalLayoutWidget_2)
        self.label_3.setText("Receiver's Email Account         ")
        self.receiver = QLineEdit(self.horizontalLayoutWidget_2)
        self.receiver.setMinimumSize(QSize(0, 40))

        self.reciever_email.addWidget(self.label_3)
        self.reciever_email.addWidget(self.receiver)

        self.horizontalLayoutWidget_3 = QWidget(self.centralwidget)
        self.horizontalLayoutWidget_3.setGeometry(QRect(10, 170, 641, 221))
        self.message_layout = QHBoxLayout(self.horizontalLayoutWidget_3)
        self.message_layout.setContentsMargins(10, 10, 10, 10)
        self.label_5 = QLabel(self.horizontalLayoutWidget_3)
        self.label_5.setText("Your message:                           ")
        self.message = QTextEdit(self.horizontalLayoutWidget_3)

        self.message_layout.addWidget(self.label_5)
        self.message_layout.addWidget(self.message)

        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(10, 460, 641, 41))
        self.label_4.setText("A tip: Just type \"default\" as Sender's email account")

        self.go_button = QPushButton(self.centralwidget)
        self.go_button.setGeometry(QRect(430, 400, 211, 31))
        self.go_button.setText("Let\'s Go")
        self.go_button.clicked.connect(lambda: self.send_email())

        self.setCentralWidget(self.centralwidget)

        self.menubar = QMenuBar(self)
        self.menubar.setGeometry(QRect(0, 0, 667, 26))
        self.setMenuBar(self.menubar)

        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)

        QMetaObject.connectSlotsByName(self)

    def send_email(self):
        sender = self.sender_email_edit.text().lower()
        receiver = self.receiver.text().lower()
        sender_message = self.message.toPlainText()

        try:
            if sender == "default":
                self.email_sender_account = "YOUR_EMAIL_ADDRESS" #Enter your email address
                self.email_sender_username = "Mail Rem"
                self.email_sender_password = "THE_PASSWORD_OF_YOUR_EMAIL_ACCOUNT" #Enter the password of your email account

                # Constants
                self.email_smtp_server = "smtp.gmail.com"
                self.email_smtp_port = 587

                # Email Content
                email_receivers = receiver
                email_subject = "Message from an anonymous user."
                email_body = sender_message

                # login to email server
                self.server = smtplib.SMTP(self.email_smtp_server, self.email_smtp_port)
                self.server.starttls()
                self.server.login(self.email_sender_account, self.email_sender_password)

                print(f"Sending email to {email_receivers}")
                message = MIMEMultipart('alternative')
                message['From'] = self.email_sender_account
                message['To'] = email_receivers
                message['Subject'] = email_subject
                message.attach(MIMEText(email_body, 'html'))
                text = message.as_string()
                self.server.sendmail(self.email_sender_account, email_receivers, text)

                # All emails sent, log out.
                self.server.quit()

        except smtplib.SMTPException:
            self.label_4.setText("Error: unable to send email")
            print("Email not sent")
            time.sleep(5)
            self.server.quit()
            sys.exit(0)

        else:
            self.label_4.setText("Please type default as the sender's email address")
            sys.exit(0)


if __name__ == '__main__':
    app = QApplication()
    window = Email()
    window.show()
    sys.exit(app.exec_())
