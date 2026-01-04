import os
import re
import sys
from PySide6.QtWidgets import (QMainWindow, QVBoxLayout, QWidget, 
                               QLabel, QProgressBar, QPushButton, QMessageBox)
from PySide6.QtCore import QProcess, Qt
from service.flatpak_service import FlatpakService

class FlatpakManager(QMainWindow):
    def __init__(self, target_url):
        super().__init__()
        self.setWindowTitle("Gerenciador Flatpak - Sandbox")
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

        self.btn_cancel = QPushButton("Cancelar")
        self.btn_cancel.clicked.connect(self.close)
        self.layout.addWidget(self.btn_cancel)

        # Processo e Serviço
        self.process = QProcess()
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.finished.connect(self.on_finished)

        self.service = FlatpakService(self.process)
        self.target_url = target_url
        self.target_base_name = os.path.basename(self.target_url)
        self.target_name = self.service.extract_name(self.target_base_name)

        self.check_status()

    def check_status(self):
        if self.service.is_installed(self.target_base_name):
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Question)
            msg_box.setWindowTitle("Aplicativo já instalado")
            msg_box.setText(f"O pacote '{self.target_name}' já está instalado no sistema.")
            msg_box.setInformativeText("Deseja removê-lo?")
            btn_sim = msg_box.addButton("Sim, desinstalar", QMessageBox.YesRole)
            btn_nao = msg_box.addButton("Não, sair", QMessageBox.NoRole)
            msg_box.exec()

            if msg_box.clickedButton() == btn_sim:
                self.start_removal()
            else:
                sys.exit(0)
            
        else:
            self.start_installation()

    def start_installation(self):
        self.label.setText(f"<b>Instalando:</b> {self.target_name} 😎")
        try:
            self.service.install(self.target_url)
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha na instalação: {e}")
            self.close()

    def start_removal(self):
        self.label.setText(f"<b>Removendo:</b> {self.target_name} 😥")
        try:
            self.service.uninstall(self.target_base_name)
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha na remoção: {e}")
            self.close()

    def handle_stdout(self):
        data = self.process.readAllStandardOutput().data().decode()
        match = re.search(r'(\d+)%', data)
        if match:
            self.current_progress.setValue(int(match.group(1)))

    def on_finished(self, exit_code):
        if exit_code == 0:
            QMessageBox.information(self, "Sucesso", "Operação concluída com êxito!")
        else:
            QMessageBox.warning(self, "Aviso", "A operação foi encerrada ou apresentou erros.")
        self.close()