from PyQt5.QtWidgets import (
    QWidget, QFormLayout, QLabel, 
    QLineEdit, QPushButton, QMessageBox
)
from banco import inserir_funcionario, verificar_cpf


class TelaCadastroFuncionarios(QWidget):
   
    def __init__(self):
        super().__init__()
        layout = QFormLayout() 

        self.input_nome = QLineEdit()
        self.input_cpf = QLineEdit()
        self.input_cargo = QLineEdit()

        layout.addRow("Nome: ", self.input_nome)
        layout.addRow("CPF: ", self.input_cpf)
        layout.addRow("Cargo: ", self.input_cargo)

        self.botao_salvar = QPushButton("Salvar")
        self.botao_salvar.clicked.connect(self.salvar_dados)

        layout.addRow(self.botao_salvar)
        self.setLayout(layout)
    
    def validar_cpf(self, cpf):
        if not cpf.isdigit() or len(cpf) != 11:
            return False
        return True

    def salvar_dados(self):
        nome = self.input_nome.text().strip()
        cpf = self.input_cpf.text().strip()
        cargo = self.input_cargo.text().strip()


        if not nome or not cpf or not cargo:
            QMessageBox.warning(self, "Erro de Preenchimento", "Todos os campos (Nome, CPF, Cargo) são obrigatórios.")
            return
        
        if not self.validar_cpf(cpf):
            QMessageBox.warning(self, "CPF Inválido", "O CPF deve conter exatamente 11 dígitos númericos.")
            return
            
        if not verificar_cpf(cpf):
            QMessageBox.warning(self, "Erro ao validar CPF", "CPF já cadastrado em outro funcionário.")
            return

        try:
            inserir_funcionario(nome, cpf, cargo)
            QMessageBox.information(self, "Sucesso", "Funcionário cadastrado com sucesso!")
            self.input_nome.clear()
            self.input_cpf.clear()
            self.input_cargo.clear()
        except Exception as e:
            QMessageBox.critical(self, "Erro ao Salvar", f"Ocorreu um erro ao salvar o funcionário: {e}\n" f"Verifique se o CPF já está cadastrado.")