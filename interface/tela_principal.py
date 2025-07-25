# interface/tela_principal.py
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel

class TelaPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Controle de EPIs")
        self.setGeometry(100, 100, 400, 300)

        self.layout = QVBoxLayout()

        self.label = QLabel("Sistema de Controle de EPIs")
        self.layout.addWidget(self.label)

        self.btn_funcionarios = QPushButton("Cadastrar Funcionários")
        self.btn_epi = QPushButton("Cadastrar EPIs")
        self.btn_entrega = QPushButton("Registrar Entrega")
        self.btn_relatorio = QPushButton("Relatórios")
        self.btn_sair = QPushButton("Sair")

        self.layout.addWidget(self.btn_funcionarios)
        self.layout.addWidget(self.btn_epi)
        self.layout.addWidget(self.btn_entrega)
        self.layout.addWidget(self.btn_relatorio)
        self.layout.addWidget(self.btn_sair)

        self.setLayout(self.layout)

        self.btn_sair.clicked.connect(self.close)
