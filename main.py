import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication
import windController
import gerbd

win = windController

banco = gerbd

app = QApplication(sys.argv)

janela = uic.loadUi("janela.ui")

windController.set_janela(janela)
banco.set_janela(janela)

janela.show()
banco.atualizar()
#comandos da tela
janela.entradabtn.clicked.connect(lambda: win.trocar_pag(0))
janela.saidabtn.clicked.connect(lambda: win.trocar_pag(1))
janela.editarbtn.clicked.connect(lambda: win.trocar_pag(2))
janela.atualizar.clicked.connect(lambda: banco.atualizar())


def salvar(tipo):
    if tipo == "entrada":
        banco.entrada(
            janela.tipoe.text(),
            janela.descricaoe.text(),
            janela.valore.text()
        )
    elif tipo == "saida":
        banco.saida(
            janela.tipos.text(),
            janela.descricaos.text(),
            janela.valors.text()
        )
    else:
        pass
    banco.atualizar_entrada()
    banco.atualizar_saida()


#entrada
janela.sentradabtn.clicked.connect(lambda: salvar("entrada"))

#saida
janela.ssaidabtn.clicked.connect(lambda: salvar("saida"))

#pesquisar
janela.buscar.clicked.connect(banco.pesquisar)
janela.salvarp.clicked.connect(banco.salvar)
janela.excluir.clicked.connect(banco.excluir)
janela.tableWidget.itemSelectionChanged.connect(banco.selecionar)
#finaliza o app
sys.exit(app.exec())