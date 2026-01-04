import sys
from PySide6.QtWidgets import (QApplication)

from ui.flatpak_manager import FlatpakManager

if __name__ == "__main__":
    app = QApplication(sys.argv)
    if len(sys.argv) < 2:
        print("Uso: flatpak-manager-gui <url/arquivo>")
        sys.exit(1)

    window = FlatpakManager(sys.argv[1])
    window.show()
    sys.exit(app.exec())
