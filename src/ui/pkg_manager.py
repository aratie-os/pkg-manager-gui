from PySide6.QtWidgets import (QMainWindow, QVBoxLayout, QWidget,
                               QLabel, QProgressBar, QPushButton, QMessageBox)
from PySide6.QtCore import QProcess, Qt


class PkgManager(QMainWindow):
    def __init__(self, title: str, other_progress_bar: QProgressBar | None = None):
        super().__init__()
        self.setWindowTitle(title)
        self.setFixedSize(500, 250)

        # UI Setup
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(20, 20, 20, 20)

        self.label = QLabel(f"<b>Verificando status...</b>")
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)

        self.current_progress = QProgressBar()
        self.current_progress.setFormat("Ação atual: %p%")
        self.layout.addWidget(self.current_progress)

        if isinstance(other_progress_bar, QProgressBar):
            self.layout.addWidget(other_progress_bar)

        self.btn_cancel = QPushButton("Cancelar")
        self.btn_cancel.clicked.connect(self.close)
        self.layout.addWidget(self.btn_cancel)

        # Processo e Serviço
        self.process = QProcess()
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.finished.connect(self.on_finished)

    def intialize_application(self):
        raise NotImplementedError(
            "Você precisa implementar este método nas subclasses!")

    def handle_stdout(self):
        raise NotImplementedError(
            "Você precisa implementar este método nas subclasses!")

    def on_finished(self, exit_code):
        if exit_code == 0:
            QMessageBox.information(
                self, "Sucesso", "Operação concluída com êxito!")
        else:
            QMessageBox.warning(
                self, "Aviso", "A operação foi encerrada ou apresentou erros.")
        self.close()
