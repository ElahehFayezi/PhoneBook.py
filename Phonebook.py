from PyQt5 import QtWidgets
import sys
import json
import os

class PhoneBookApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Telefonbuch")

        # Zentrales Widget und Layout
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout_main = QtWidgets.QVBoxLayout(central)

        # Eingabefelder für Name und Telefonnummer
        input_layout = QtWidgets.QHBoxLayout()
        self.lineName = QtWidgets.QLineEdit()
        self.lineName.setPlaceholderText("Name")
        self.linePhone = QtWidgets.QLineEdit()
        self.linePhone.setPlaceholderText("Telefonnummer")
        input_layout.addWidget(self.lineName)
        input_layout.addWidget(self.linePhone)
        layout_main.addLayout(input_layout)

        # Buttons zum Hinzufügen und Löschen
        button_layout = QtWidgets.QHBoxLayout()
        self.btnAdd = QtWidgets.QPushButton("Hinzufügen")
        self.btnDelete = QtWidgets.QPushButton("Löschen")
        button_layout.addWidget(self.btnAdd)
        button_layout.addWidget(self.btnDelete)
        layout_main.addLayout(button_layout)

        # Liste der Kontakte
        self.listContacts = QtWidgets.QListWidget()
        layout_main.addWidget(self.listContacts)

        # Signale verbinden
        self.btnAdd.clicked.connect(self.add_contact)
        self.btnDelete.clicked.connect(self.delete_contact)
        self.listContacts.itemClicked.connect(self.display_contact)

        # Kontakte laden
        self.contacts = []
        self.load_contacts()

    def add_contact(self):
        name = self.lineName.text().strip()
        phone = self.linePhone.text().strip()
        if name and phone:
            contact = {"name": name, "phone": phone}
            self.contacts.append(contact)
            self.listContacts.addItem(f"{name} – {phone}")
            self.lineName.clear()
            self.linePhone.clear()
            self.save_contacts()

    def delete_contact(self):
        current = self.listContacts.currentRow()
        if current >= 0:
            self.contacts.pop(current)
            self.listContacts.takeItem(current)
            self.lineName.clear()
            self.linePhone.clear()
            self.save_contacts()

    def display_contact(self, item):
        text = item.text()
        if '–' in text:
            name, phone = text.split('–')
            self.lineName.setText(name.strip())
            self.linePhone.setText(phone.strip())

    def load_contacts(self):
        if os.path.exists("contacts.json"):
            with open("contacts.json", "r", encoding="utf-8") as f:
                self.contacts = json.load(f)
            for c in self.contacts:
                self.listContacts.addItem(f"{c['name']} – {c['phone']}")

    def save_contacts(self):
        with open("contacts.json", "w", encoding="utf-8") as f:
            json.dump(self.contacts, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = PhoneBookApp()
    window.show()
    sys.exit(app.exec_())
