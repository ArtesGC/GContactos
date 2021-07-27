from os import makedirs, path
from sys import argv, exit
import sqlite3

from PyQt5.Qt import *
from gcdatabase import GCdb


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
        ler.triggered.connect(self._ler)
        # ------------------------------
        _sair = lambda: exit(0)
        sair = detalhes.addAction('Sair')
        sair.triggered.connect(_sair)
        # ------------------------------
        sobre = menu.addAction('Sobre')
        sobre.triggered.connect(self._sobre)

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

        btnProcurar = QLineEdit()
        btnProcurar.setPlaceholderText('Digite o nome ou numero do contacto..')
        layout.addRow(btnProcurar)

        conectDb = QSqlDatabase.addDatabase('QSQLITE')
        conectDb.setDatabaseName('Contactos/gc.db')

        modelDb = QSqlTableModel()
        modelDb.setTable('gcontactos')
        modelDb.setHeaderData(0, Qt.Horizontal, 'Nome')
        modelDb.setHeaderData(1, Qt.Horizontal, 'Numero')
        modelDb.setHeaderData(2, Qt.Horizontal, 'Email')
        modelDb.setHeaderData(3, Qt.Horizontal, 'Morada')

        tabelaContactos = QTableView()
        tabelaContactos.setModel(modelDb)
        tabelaContactos.setAlternatingRowColors(True)
        tabelaContactos.setSortingEnabled(True)
        tabelaContactos.resizeColumnsToContents()
        tabelaContactos.clicked.connect(self._editar)
        layout.addRow(tabelaContactos)

        janela1.setLayout(layout)
        self.tab.addTab(janela1, 'Principal')
        self.tab.setCurrentIndex(self.tab.currentIndex())

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
            pass

    #
    def _editar(self):
        pass

    def editar(self):
        pass

    def _ler(self):
        pass

    def _sobre(self):
        QMessageBox.information(self.ferramentas, 'Sobre o Programa', f"""
Nome: GContactos
Versão: 0.7-082021
Designer e Programador: Nurul GC
Empresa: ArtesGC Inc.""")


if __name__ == '__main__':
    GCdb().conectarDb()
    app = GContactos()
    app.ferramentas.show()
    app.gc.exec_()
