import os
import subprocess
from dotenv import load_dotenv

load_dotenv()

APP_NAME = os.getenv("APP_NAME")
VERSION = os.getenv("VERSION")
MAINTAINER = os.getenv("MAINTAINER")

def build():
    print("--- Iniciando Build do ELF ---")
    """
      # Gerar o ELF único usando PyInstaller
      # --onefile: executável único
      # --windowed: não abre terminal ao fundo
    """
    subprocess.run([
        "pyinstaller", "--onefile", "--windowed", 
        f"--name={APP_NAME}", "./src/main.py"
    ], check=True)

    print("--- Criando estrutura do pacote DEB ---")
    working_dir = f"/tmp/{APP_NAME}-build"
    os.makedirs(f"{working_dir}/DEBIAN", exist_ok=True)
    os.makedirs(f"{working_dir}/usr/bin", exist_ok=True)

    # Copia o ELF gerado para a pasta bin do deb
    subprocess.run(["cp", f"dist/{APP_NAME}", f"{working_dir}/usr/bin/"], check=True)

    control_content = f"""Package: {APP_NAME}
Version: {VERSION}
Section: utils
Priority: optional
Architecture: amd64
Maintainer: {MAINTAINER}
Depends: flatpak
Description: {os.getenv("DESCRIPTION")}
"""
    with open(f"{working_dir}/DEBIAN/control", "w") as f:
        f.write(control_content)

    # Gerar o .deb
    subprocess.run(["dpkg-deb", "--build", working_dir, f"./dist/{APP_NAME}.deb"], check=True)
    print(f"--- Sucesso: {APP_NAME}.deb gerado! ---")

if __name__ == "__main__":
    build()