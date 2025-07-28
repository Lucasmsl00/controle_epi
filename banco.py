# banco.py
import sqlite3

def criar_banco():
    conn = sqlite3.connect("controle_epi.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS funcionarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cpf TEXT NOT NULL UNIQUE, -- Adicione UNIQUE para CPF
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

def verificar_cpf(cpf):
    conn = sqlite3.connect("controle_epi.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM funcionarios WHERE cpf = ?", (cpf,))
    count = cursor.fetchone()[0]
    conn.close()
    return count == 0

def inserir_funcionario(nome, cpf, cargo):
    conn = sqlite3.connect("controle_epi.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO funcionarios (nome, cpf, cargo) VALUES (?, ?, ?)", (nome, cpf, cargo))
    conn.commit()
    conn.close()

def buscar_funcionarios():
    conn = sqlite3.connect("controle_epi.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, cpf, cargo FROM funcionarios")
    funcionarios = cursor.fetchall() # Pega todos os resultados
    conn.close()
    return funcionarios

def atualizar_funcionario(id_funcionario, novo_nome, novo_cpf, novo_cargo):
    conn = sqlite3.connect("controle_epi.db")
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE funcionarios
            SET nome = ?, cpf = ?, cargo = ?
            WHERE id = ?
        """, (novo_nome, novo_cpf, novo_cargo, id_funcionario))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    except Exception:
        return False
    finally:
        conn.close()