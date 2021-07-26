from os import makedirs, path
from sys import argv
import sqlite3

from PyQt5.Qt import *


class GContactos:
    def __init__(self):
        self.gc = QApplication(argv)
        self.ferramentas = QWidget()
        self.ferramentas.setFixedSize(550, 500)
        self.ferramentas.setWindowIcon(QIcon("img/artesgc.png"))
        self.ferramentas.setWindowTitle('Contactos GC')
        self.ferramentas.setPalette(QPalette(QColor('antiquewhite')))

        menu = QMenuBar(self.ferramentas)
        detalhes = menu.addMenu('Opções')
        # ------------------------------
        ler = detalhes.addAction('Ler Contacto')
        ler.triggered.connect(self.ler)
        # ------------------------------
        editar = detalhes.addAction('Editar Contacto')
        editar.triggered.connect(self.editar)
        detalhes.addSeparator()
        # ------------------------------
        _sair_ = lambda: self.gc.instance().exit(0)
        sair = detalhes.addAction('Sair')
        sair.triggered.connect(_sair_)
        # ------------------------------
        sobre = menu.addAction('Sobre')
        sobre.triggered.connect(self.sobre)

        self.tab = QTabWidget(self.ferramentas)
        self.tab.setFixedSize(550, 480)
        self.tab.move(0, 25)

        self.nome = None
        self.numero = None
        self.endereco1 = None
        self.endereco2 = None
        self.email = None

        self.principal()

    def principal(self):
        janela1 = QWidget()
        layout = QFormLayout()
        layout.setSpacing(15)

    def _guardar(self):
        self.tab.removeTab(0)
        self.principal()
        self.nome.clear()
        self.numero.clear()
        self.endereco1.clear()
        self.endereco2.clear()
        self.email.clear()

    def guardar(self):
        if (self.nome and self.numero) is None:
            QMessageBox.warning(self.ferramentas, 'Atenção', 'Contacto Não Guardado\n- Nome e Número Não Preenchidos..')
        elif (self.nome.text() and self.numero.text()) == '':
            QMessageBox.warning(self.ferramentas, 'Atenção', 'Contacto Não Guardado\n- Nome e Número Não Preenchidos..')
        else:
            if not path.exists('Contactos'):
                makedirs('Contactos')

    #
    def _editar(self):
        if self.janela2 is None:
            return self.editar()
        try:
            self.tab.removeTab(1)
            return self.editar()
        except Exception:
            return self.editar()

    def editar(self):
        pass

    def sobre(self):
        QMessageBox.information(self.ferramentas, 'Sobre o Programa', f"""
Nome: GContactos
Versão: 0.7-082021
Designer e Programador: Nurul GC
Empresa: ArtesGC Inc.""")


class GCdb:
    """classe para gerir as operacoes com a db"""
    def criarDb(self):
        makedirs('Contactos', exist_ok=True)
        try:
            db = sqlite3.connect('Contactos/gc.db')
            executor = db.cursor()
        except Exception as erro:
            print(f'[X]-{erro}')

    def redefinirDb(self):
        pass

    def guardarNovosDados(self, _nome, _numero, _email, _morada):
        pass


if __name__ == '__main__':
    app = GContactos()
    app.ferramentas.show()
    app.gc.exec_()
