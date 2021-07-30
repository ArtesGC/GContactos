from sys import argv, exit

from PyQt5.Qt import *

from gcdatabase import GCdb

theme = open('themes/gcontactos.qss').read().strip()


class GContactos:
    def __init__(self):
        self.gc = QApplication(argv)
        self.ferramentas = QWidget()
        self.ferramentas.setFixedSize(550, 500)
        self.ferramentas.setWindowIcon(QIcon("img/artesgc.png"))
        self.ferramentas.setWindowTitle('GContactos')
        self.ferramentas.setStyleSheet(theme)

        menu = QToolBar(self.ferramentas)

        sobre = menu.addAction(QIcon("img/icons/about.png"), 'Sobre')
        sobre.triggered.connect(self._sobre)

        _sair = lambda: exit(0)
        sair = menu.addAction(QIcon("img/icons/close.png"), 'Sair')
        sair.triggered.connect(_sair)

        self.tab = QTabWidget(self.ferramentas)
        self.tab.setGeometry(0, 50, 550, 470)

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
