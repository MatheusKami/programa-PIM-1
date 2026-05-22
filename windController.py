janela = None


def set_janela(j):
    global janela
    janela = j


def trocar_pag(num):
    janela.corpo.setCurrentIndex(num)