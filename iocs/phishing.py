import sys

from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QTextEdit, QLabel, QFileDialog, QListWidget
import pytesseract
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials


class Widget(QWidget):
    def __init__(self):
        super().__init__()

        # setting window size
        self.setMinimumSize(900, 700)
        self.setMaximumSize(900, 700)
        self.setFixedSize(900, 700)

        # setting icon
        icon = QIcon('phishing.jpg')
        self.setWindowIcon(icon)

        # setting font
        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(True)
        self.setFont(font)

        # setting window title
        self.setWindowTitle("Phishing IOCs")

        # align layout
        self.layout = QHBoxLayout()
        self.v_layout = QVBoxLayout()
        self.h_layout = QHBoxLayout()

        # declare ListWidget
        self.list_widget = QListWidget()
        self.layout.addWidget(self.list_widget)

        # declare upload and detect button
        upload_btn = QPushButton('Gmail API')
        detect_btn = QPushButton('Detect Phishing IOCs')
        upload_btn.setSizeIncrement(100, 30)
        detect_btn.setSizeIncrement(100, 30)
        self.h_layout.addWidget(upload_btn)
        self.h_layout.addWidget(detect_btn)
        self.v_layout.addLayout(self.h_layout)

        # declare header and content textedit
        header_label = QLabel("Header")
        self.header_edit = QTextEdit()
        content_label = QLabel("Content")
        self.content_edit = QTextEdit()
        self.v_layout.addWidget(header_label)
        self.v_layout.addWidget(self.header_edit)
        self.v_layout.addWidget(content_label)
        self.v_layout.addWidget(self.content_edit)
        self.layout.addLayout(self.v_layout)

        self.setLayout(self.layout)
        self.show()

        # signal and slot
        upload_btn.clicked.connect(self.analyze_gmail_messages())

    def analyze_gmail_messages(self):
        print("analyze gmail message")
        # Load credentials from credentials.json
        creds = Credentials.from_authorized_user_file('client_secret_262693570533-ti7tntl3jcsfh4ai8g8vc5a3eml72ssn.apps.googleusercontent.com.json')

        # Build the Gmail service
        service = build('gmail', 'v1', credentials=creds)

        # Retrieve the list of messages
        results = service.users().messages().list(userId='me').execute()
        messages = results.get('messages', [])

        # Analyze each message
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()

            # Extract the header
            header = msg['payload']['headers']

            # Extract the content
            parts = msg['payload']['parts']
            content = ""
            for part in parts:
                if part['mimeType'] == 'text/plain':
                    data = part['body'].get('data')
                    if data:
                        content = data
                        break

            # Print the header and content
            print("Header:")
            for item in header:
                print(f"{item['name']}: {item['value']}")

            print("\nContent:")
            print(content)
            print("--------------------------------------------------")

    def email_view(self, header, content):
        self.header_edit.setText(header)
        self.header_edit.setText(content)

    def detect_phishing_iocs(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = Widget()
    window.show()

    app.exec()
