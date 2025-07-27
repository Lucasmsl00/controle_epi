import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout,
    QMenuBar, QMenu, QAction, QMessageBox
)
from interface.tela_cadastro_funcionario import TelaCadastroFuncionario
from interface.tela_listar_funcionario import TelaListarFuncionario
from licenca import verificar_licenca
from banco import criar_banco 


criar_banco()

class TelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Controle de EPIs")
        self.setGeometry(100, 100, 800, 600)

        self.widget_central = QWidget()
        self.setCentralWidget(self.widget_central)

        self.layout = QVBoxLayout()
        self.widget_central.setLayout(self.layout)


        self.criar_menu()


    def criar_menu(self):
        
        # Criando Menu
        barra_menu = self.menuBar()

        # Menu Funcionários
        menu_func = barra_menu.addMenu("Funcionários")
        acao_cad_func = QAction("Cadastrar Funcionário", self)
        acao_list_func = QAction("Listar Funcionários", self)
        menu_func.addAction(acao_cad_func)
        menu_func.addAction(acao_list_func)

        # Menu EPIs
        menu_epi = barra_menu.addMenu("EPIs")
        acao_cad_epi = QAction("Cadastrar EPI", self)
        menu_epi.addAction(acao_cad_epi)

        # Menu Entregas
        menu_entrega = barra_menu.addMenu("Entregas")
        acao_entregar = QAction("Registrar entrega", self)
        menu_entrega.addAction(acao_entregar)

        # Menu Relatórios
        menu_relatorio = barra_menu.addMenu("Relatórios")
        acao_relatorio = QAction("Gerar Relatório", self)
        menu_relatorio.addAction(acao_relatorio)

        # Conectando ações do menu às funções
        acao_cad_func.triggered.connect(self.tela_cadastrar_funcionario)
        acao_list_func.triggered.connect(self.tela_listar_funcionario)
        acao_cad_epi.triggered.connect(self.tela_cadastrar_epi)
        acao_entregar.triggered.connect(self.tela_registrar_entrega)
        acao_relatorio.triggered.connect(self.tela_relatorio)

    def tela_cadastrar_funcionario(self):
        self.limpar_layout()
        self.tela_funcionario = TelaCadastroFuncionario()
        self.layout.addWidget(self.tela_funcionario)

    def tela_listar_funcionario(self):
        self.limpar_layout()
        self.tela_listagem_func = TelaListarFuncionario()
        self.layout.addWidget(self.tela_listagem_func)


    def tela_cadastrar_epi(self):
        self.limpar_layout()
        self.layout.addWidget(QLabel("Tela de Cadastro de EPI (Em Breve!)"))

    def tela_registrar_entrega(self):
        self.limpar_layout()
        self.layout.addWidget(QLabel("Tela de Registro de Entrega de EPI (Em Breve!)"))

    def tela_relatorio(self):
        self.limpar_layout()
        self.layout.addWidget(QLabel("Tela de Relatório de EPIs Entregues (Em Breve!)"))
    
    def limpar_layout(self):
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()


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