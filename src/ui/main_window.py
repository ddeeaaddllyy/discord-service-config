from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton,
    QListWidget, QLabel, QFileDialog
)
from src.core.scanner import find_git_projects

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("KISS")
        self.resize(800, 600)

        self.layout = QVBoxLayout()

        self.label = QLabel("Projects")
        self.list_widget = QListWidget()

        self.scan_btn = QPushButton("Scan Projects")
        self.commit_btn = QPushButton("Commit All")

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.list_widget)
        self.layout.addWidget(self.scan_btn)
        self.layout.addWidget(self.commit_btn)

        self.setLayout(self.layout)

        self.scan_btn.clicked.connect(self.scan_projects)
        self.commit_btn.clicked.connect(self.commit_all)

        self.projects = []

    def scan_projects(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if not folder:
            return

        self.projects = find_git_projects([folder])
        self.list_widget.clear()

        for proj in self.projects:
            status = proj["git"].status()
            text = f"{proj['path']} | {len(status)} changes"
            self.list_widget.addItem(text)

    def commit_all(self):
        for proj in self.projects:
            git = proj["git"]
            git.add_all()
            git.commit("Auto commit from KISS")
            git.push()