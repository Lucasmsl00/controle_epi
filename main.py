# main.py
import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from interface.tela_principal import TelaPrincipal
from licenca import verificar_licenca
from banco import criar_banco

def main():
    app = QApplication(sys.argv)

    if not verificar_licenca():
        QMessageBox.critical(None, "Licença inválida", "Licença expirada, inválida ou sem verificação recente.")
        sys.exit(1)

    criar_banco()  # Cria o banco e tabelas, se ainda não existirem

    janela = TelaPrincipal()
    janela.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
