from PyQt5.QtWidgets import *
from PyQt5 import uic
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart


class MyGUI(QMainWindow):

    def __init__(self):
        super(MyGUI, self).__init__()
        uic.loadUi('untitled.ui', self)
        self.show()

        self.btnLogin.clicked.connect(self.login)
        self.btnAdd.clicked.connect(self.attach_something)
        self.btnSend.clicked.connect(self.send_mail)

    def login(self):
        try:
            self.server = smtplib.SMTP(self.leSMTP.text(), self.lePort.text())
            self.server.ehlo()  # check if it works
            self.server.starttls()  # for the encryption
            self.server.ehlo()
            self.server.login(self.leMail.text(), self.lePassword.text())

            self.leMail.setEnabled(False)
            self.lePassword.setEnabled(False)
            self.leSMTP.setEnabled(False)
            self.lePort.setEnabled(False)
            self.btnLogin.setEnabled(False)

            self.leFrom.setEnabled(True)
            self.leTo.setEnabled(True)
            self.leSubject.setEnabled(True)
            self.teText.setEnabled(True)
            self.btnAdd.setEnabled(True)
            self.btnSend.setEnabled(True)

            self.msg = MIMEMultipart()
        except smtplib.SMTPAuthenticationError:
            message_box = QMessageBox()
            message_box.setText("Invalid Login Info!")
            message_box.exec_()
        except:
            message_box = QMessageBox()
            message_box.setText("Login Failed!")
            message_box.exec_()

    def attach_something(self):
        options = QFileDialog.Options()
        filenames, _ = QFileDialog.getOpenFileNames(self, "Open File", "", "All Files(*.*)", options=options)
        if filenames != []:
            for filename in filenames:
                attachment = open(filename, 'rb')

                filename = filename[filename.rfind("/") + 1:]

                p = MIMEBase('application', 'octet-stream')
                p.set_payload(attachment.read())
                encoders.encode_base64(p)
                p.add_header('Content-Disposition', f"attachment; filename={filename}")
                self.msg.attach(p)
                if not self.lAttachments.text().endswith(":"):
                    self.lAttachments.setText(self.lAttachments.text() + ",")
                self.lAttachments.setText(self.lAttachments.text() + " " + filename)

    def send_mail(self):
        dialog = QMessageBox()
        dialog.setText("Do you want to send this mail?")
        dialog.addButton(QPushButton("Yes"), QMessageBox.YesRole)  # 0
        dialog.addButton(QPushButton("No"), QMessageBox.NoRole)  # 1

        if dialog.exec_() == 0:
            try:
                self.msg['From'] = self.leFrom.text()
                self.msg['To'] = self.leTo.text()
                self.msg['Subject'] = self.leSubject.text()
                self.msg.attach(MIMEText(self.teText.toPlainText(), 'plain'))
                text = self.msg.as_string()
                self.server.sendmail(self.leMail.text(), self.leTo.text(), text)
                message_box = QMessageBox()
                message_box.setText("Mail sent!")
                message_box.exec_()
            except:
                message_box = QMessageBox()
                message_box.setText("Something went wrong!")
                message_box.exec_()


def main():
    app = QApplication([])
    window = MyGUI()
    app.exec_()


if __name__ == "__main__":
    main()
