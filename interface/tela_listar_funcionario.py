from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QMessageBox
)
from banco import buscar_funcionarios

class TelaListarFuncionario(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Listar Funcionários")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.tabela_funcionarios = QTableWidget()
        self.layout.addWidget(self.tabela_funcionarios)

        self.tabela_funcionarios.setColumnCount(4)
        self.tabela_funcionarios.setHorizontalHeaderLabels(["ID", "Nome", "CPF", "Cargo"])
        self.tabela_funcionarios.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabela_funcionarios.setSelectionBehavior(QTableWidget.SelectRows)

        self.btn_atualizar = QPushButton("Atualizar Lista")
        self.btn_atualizar.clicked.connect(self.carregar_dados)
        self.layout.addWidget(self.btn_atualizar)


        self.carregar_dados()

    
    def carregar_dados(self):
        self.tabela_funcionarios.setRowCount(0)
        funcionarios = buscar_funcionarios()

        if funcionarios:
            self.tabela_funcionarios.setRowCount(len(funcionarios))
            for row, funcionarios in enumerate(funcionarios):
                self.tabela_funcionarios.setItem(row, 0, QTableWidgetItem(str(funcionarios[0])))  # ID
                self.tabela_funcionarios.setItem(row, 1, QTableWidgetItem(funcionarios[1]))  # Nome
                self.tabela_funcionarios.setItem(row, 2, QTableWidgetItem(funcionarios[2]))  # CPF
                self.tabela_funcionarios.setItem(row, 3, QTableWidgetItem(funcionarios[3] if funcionarios[3] else "N/A"))

            self.tabela_funcionarios.resizeColumnsToContents()

        else:
            QMessageBox.information(self, "Informação", "Nenhum funcionário cadastrado.")
