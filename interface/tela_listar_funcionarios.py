from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QMessageBox, QHeaderView
)
from banco import buscar_funcionarios

class TelaListarFuncionarios(QWidget):
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

        self.tabela_funcionarios.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        botoes_layout = QHBoxLayout()

        self.btn_atualizar = QPushButton("Atualizar Lista")
        self.btn_atualizar.clicked.connect(self.carregar_dados)
        self.layout.addWidget(self.btn_atualizar)

        self.btn_editar = QPushButton("Editar Funcionário Selecionado")
        self.btn_editar.clicked.connect(self.editar_funcionario)
        botoes_layout.addWidget(self.btn_editar)

        self.layout.addLayout(botoes_layout)
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
                self.tabela_funcionarios.setItem(row, 3, QTableWidgetItem(funcionarios[3] if funcionarios[3] else "N/A")) # Cargo


        else:
            QMessageBox.information(self, "Informação", "Nenhum funcionário cadastrado ainda.")
    
    def editar_funcionario(self):
        selected_items = self.tabela_funcionarios.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Nenhuma Seleção", "Por favor, selecione um funcionário para editar.")
            return
        
        linha_selecionada = selected_items[0].row()

        id_func = int(self.tabela_funcionarios.item(linha_selecionada, 0).text())
        nome_func = self.tabela_funcionarios.item(linha_selecionada, 1).text()
        cpf_func = self.tabela_funcionarios.item(linha_selecionada, 2).text()
        cargo_func = self.tabela_funcionarios.item(linha_selecionada, 3).text()

        from interface.tela_editar_funcionarios import TelaEditarFuncionarios
        self.tela_editar = TelaEditarFuncionarios(id_func, nome_func, cpf_func, cargo_func)
        self.tela_editar.funcionario_editado.connect(self.carregar_dados)
        self.tela_editar.show()
