import os
import re
import sys
from PySide6.QtWidgets import (QMessageBox)
from service.flatpak_service import FlatpakService
from ui.pkg_manager import PkgManager


class FlatpakManager(PkgManager):
    def __init__(self, target_url):
        super().__init__(title="Flatpak Manager")

        self.service = FlatpakService(self.process)
        self.target_url = target_url
        self.target_base_name = os.path.basename(self.target_url)
        self.target_name = self.service.extract_name(self.target_base_name)

        self.intialize_application()

    def intialize_application(self):
        if self.service.is_installed(self.target_base_name):
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Question)
            msg_box.setWindowTitle("Aplicativo já instalado")
            msg_box.setText(
                f"O pacote '{self.target_name}' já está instalado no sistema.")
            msg_box.setInformativeText("Deseja removê-lo?")
            btn_sim = msg_box.addButton(
                "Sim, desinstalar", QMessageBox.YesRole)
            msg_box.addButton("Não, sair", QMessageBox.NoRole)
            msg_box.exec()

            if msg_box.clickedButton() == btn_sim:
                self._start_removal()
            else:
                sys.exit(0)

        else:
            self._start_installation()

    def _start_installation(self):
        self.label.setText(f"<b>Instalando:</b> {self.target_name} 😎")
        try:
            self.service.install(self.target_url)
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha na instalação: {e}")
            self.close()

    def _start_removal(self):
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
