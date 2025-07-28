from PyQt5.QtWidgets import (
    QWidget, QFormLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox
)
from PyQt5.QtCore import pyqtSignal
from banco import atualizar_funcionario, verificar_cpf

class TelaEditarFuncionarios(QWidget):
    funcionario_editado = pyqtSignal()
    def __init__(self, id_funcionario, nome_atual, cpf_atual, cargo_atual):
        super().__init__()
        self.id_funcionario = id_funcionario
        self.setWindowTitle("Editar Funcionário: {}".format(nome_atual))
        self.setMinimumSize(300, 200)
        self.setGeometry(100, 100, 300, 200)

        layout = QFormLayout()

        self.input_nome = QLineEdit(nome_atual)
        self.input_cpf = QLineEdit(cpf_atual)
        self.input_cargo = QLineEdit(cargo_atual)

        layout.addRow("Nome: ", self.input_nome)
        layout.addRow("CPF: ", self.input_cpf)
        layout.addRow("Cargo: ", self.input_cargo)

        self.botao_salvar = QPushButton("Salvar Alterações")
        self.botao_salvar.clicked.connect(self.salvar_alteracoes)

        layout.addRow(self.botao_salvar)
        self.setLayout(layout)

    def validar_cpf(self, cpf):
        if not cpf.isdigit() or len(cpf) != 11:
            return False
        return True
    

    def salvar_alteracoes(self):
        novo_nome = self.input_nome.text().strip()
        novo_cpf = self.input_cpf.text().strip()
        novo_cargo = self.input_cargo.text().strip()

        if not novo_nome or not novo_cpf or not novo_cargo:
            QMessageBox.warning(self, "Erro de Preenchimento", "Todos os campos (Nome, CPF, Cargo) são obrigatórios.")
            return

        if not self.validar_cpf(novo_cpf):
            QMessageBox.warning(self, "CPF Inválido", "O CPF deve conter exatamente 11 dígitos numéricos.")
            return

        if novo_cpf != self.input_cpf.text():
            if not verificar_cpf(novo_cpf):
                QMessageBox.warning(self, "Erro ao validar CPF", "CPF já cadastrado em outro funcionário.")
                return
        
        if atualizar_funcionario(self.id_funcionario, novo_nome, novo_cpf, novo_cargo):
            QMessageBox.information(self, "Sucesso", "Funcionário atualizado com sucesso!")
            self.funcionario_editado.emit()
            self.close()
        else:
            QMessageBox.critical(self, "Erro ao Atualizar", "Ocorreu um erro ao salvar as alterações. Verifique se o CPF já está cadastrado.")