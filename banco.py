# banco.py
import sqlite3

def criar_banco():
    conn = sqlite3.connect("controle_epi.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS funcionarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cpf TEXT NOT NULL,
        cargo TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS epis (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        descricao TEXT NOT NULL,
        validade_meses INTEGER NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS entregas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        funcionario_id INTEGER NOT NULL,
        epi_id INTEGER NOT NULL,
        data_entrega TEXT NOT NULL,
        FOREIGN KEY (funcionario_id) REFERENCES funcionarios(id),
        FOREIGN KEY (epi_id) REFERENCES epis(id)
    );
    """)

    conn.commit()
    conn.close()
