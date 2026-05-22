import sqlite3
from PyQt6.QtWidgets import QTableWidgetItem

# cria bd ou abre se existir
conexao = sqlite3.connect("sistema.db")

cursor = conexao.cursor()

def set_janela(j):
    global janela
    janela = j


#criar tabelas
cursor.execute("""
CREATE TABLE IF NOT EXISTS entradas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT,
    descricao TEXT,
    valor REAL
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS saidas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT,
    descricao TEXT,
    valor REAL
)
""")

conexao.commit()


#adicionar item entrada
def entrada(tipo, descricao, valor):
        cursor.execute("""
        INSERT INTO entradas
        (tipo, descricao, valor)
        VALUES (?, ?, ?)
        """, (
            tipo,
            descricao,
            valor
        ))
        conexao.commit()
        atualizar_saldo()

def atualizar_entrada():
        cursor.execute("SELECT * FROM entradas")
        dados = cursor.fetchall()

        # quantidade de linhas
        janela.tabelae.setRowCount(len(dados))

        # preencher
        for linha in range(len(dados)):

            for coluna in range(len(dados[linha])):

                item = QTableWidgetItem(
                    str(dados[linha][coluna])
                )

                janela.tabelae.setItem(
                    linha,
                    coluna,
                    item
                )


def atualizar_saida():
        cursor.execute("SELECT * FROM saidas")
        dados = cursor.fetchall()

        # quantidade de linhas
        janela.tabelas.setRowCount(len(dados))

        # preencher
        for linha in range(len(dados)):

            for coluna in range(len(dados[linha])):

                item = QTableWidgetItem(
                    str(dados[linha][coluna])
                )

                janela.tabelas.setItem(
                    linha,
                    coluna,
                    item
                )
      

#geral
def atualizar():
      atualizar_entrada()
      atualizar_saida()
      atualizar_saldo()

#adicionar item saida
def saida(tipo, descricao, valor):
        
        cursor.execute("""
        INSERT INTO saidas
        (tipo, descricao, valor)
        VALUES (?, ?, ?)
        """, (
            tipo,
            descricao,
            valor
        ))
        conexao.commit()
        atualizar_saldo()

def pesquisar():

    busca = (
        janela.Id.text()
        or janela.tiposo.text()
        or janela.descricaop.text()
        or janela.valorp.text()
    )

    cursor.execute("""
        SELECT * FROM entradas
        WHERE
            CAST(id AS TEXT) LIKE ?
            OR tipo LIKE ?
            OR descricao LIKE ?
            OR CAST(valor AS TEXT) LIKE ?

        UNION ALL

        SELECT * FROM saidas
        WHERE
            CAST(id AS TEXT) LIKE ?
            OR tipo LIKE ?
            OR descricao LIKE ?
            OR CAST(valor AS TEXT) LIKE ?
    """, (

        f"%{busca}%",
        f"%{busca}%",
        f"%{busca}%",
        f"%{busca}%",

        f"%{busca}%",
        f"%{busca}%",
        f"%{busca}%",
        f"%{busca}%"
    ))

    dados = cursor.fetchall()

    janela.tableWidget.clearContents()

    janela.tableWidget.setColumnCount(4)
    janela.tableWidget.setRowCount(len(dados))

    for linha in range(len(dados)):

        for coluna in range(len(dados[linha])):

            item = QTableWidgetItem(
                str(dados[linha][coluna])
            )

            janela.tableWidget.setItem(
                linha,
                coluna,
                item
            )

    janela.tableWidget.resizeColumnsToContents()

def selecionar():

    linha = janela.tableWidget.currentRow()

    if linha < 0:
        return

    janela.Id.setText(
        janela.tableWidget.item(linha, 0).text()
    )

    janela.tiposo.setText(
        janela.tableWidget.item(linha, 1).text()
    )

    janela.descricaop.setText(
        janela.tableWidget.item(linha, 2).text()
    )

    janela.valorp.setText(
        janela.tableWidget.item(linha, 3).text()
    )

def salvar():

    id = janela.Id.text()

    tipo = janela.tiposo.text()
    descricao = janela.descricaop.text()
    valor = janela.valorp.text()

    # tenta entradas
    cursor.execute("""
        UPDATE entradas
        SET
            tipo=?,
            descricao=?,
            valor=?
        WHERE id=?
    """, (
        tipo,
        descricao,
        valor,
        id
    ))

    # se não encontrou
    if cursor.rowcount == 0:

        cursor.execute("""
            UPDATE saidas
            SET
                tipo=?,
                descricao=?,
                valor=?
            WHERE id=?
        """, (
            tipo,
            descricao,
            valor,
            id
        ))

    conexao.commit()
    atualizar_saldo()

    print("Atualizado")

def excluir():


    id = janela.Id.text()

    cursor.execute("""
        DELETE FROM entradas
        WHERE id=?
    """, (id,))

    apagou = cursor.rowcount

    if apagou == 0:

        cursor.execute("""
            DELETE FROM saidas
            WHERE id=?
        """, (id,))

    conexao.commit()
    atualizar_saldo()
    janela.Id.clear()
    janela.tiposo.clear()
    janela.descricaop.clear()
    janela.valorp.clear()

    print("Registro excluído")

#calculo
def calcular():


    cursor.execute("""
        SELECT SUM(valor)
        FROM entradas
    """)

    total_entrada = cursor.fetchone()[0]

    cursor.execute("""
        SELECT SUM(valor)
        FROM saidas
    """)

    total_saida = cursor.fetchone()[0]

    # evita None
    if total_entrada is None:
        total_entrada = 0

    if total_saida is None:
        total_saida = 0

    saldo = float(total_entrada) - float(total_saida)

    return saldo

def atualizar_saldo():

    saldo = calcular()

    janela.saldo.setText(
        f"R$ {saldo:.2f}"
    )