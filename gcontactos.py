import re
from sys import argv, exit

from PyQt5.Qt import *

from gcdatabase import GCdb
from gcindicativos import GCI

theme = open('themes/gcontactos.qss').read().strip()


class GContactos:
    def __init__(self):
        self.gc = QApplication(argv)
        self.ferramentas = QWidget()
        self.ferramentas.setFixedSize(600, 600)
        self.ferramentas.setWindowIcon(QIcon("img/artesgc.png"))
        self.ferramentas.setWindowTitle('GContactos')
        self.ferramentas.setStyleSheet(theme)

        menu = QToolBar(self.ferramentas)

        _sair = lambda: exit(0)
        sair = menu.addAction(QIcon("img/icons/rempage.png"), 'Fechar')
        sair.triggered.connect(_sair)

        novo = menu.addAction(QIcon('img/icons/newcontact.png'), 'Novo Contacto')
        novo.triggered.connect(self._novo)

        sobre = menu.addAction(QIcon("img/icons/about.png"), 'Sobre')
        sobre.triggered.connect(self._sobre)

        self.tab = QTabWidget(self.ferramentas)
        self.tab.setGeometry(0, 40, 600, 570)

        self.nome = None
        self.numero = None
        self.endereco = None
        self.email = None
        self.indicativo = None
        self.janelaNovoContacto = None
        self.janelaEditarContacto = None
        self.janelaLerContacto = None

        self.principal()

    def principal(self):
        janela1 = QWidget()
        layout = QFormLayout()
        layout.setSpacing(15)

        janela1.setLayout(layout)
        self.tab.addTab(janela1, 'Principal')
        self.tab.setCurrentIndex(self.tab.currentIndex())

    def _editar(self):
        if not self.janelaEditarContacto:
            return self.editar()
        else:
            return self.tab.setCurrentWidget(self.janelaEditarContacto)

    def editar(self):
        pass

    def _ler(self):
        if not self.janelaLerContacto:
            return self.ler()
        else:
            return self.tab.setCurrentWidget(self.janelaLerContacto)

    def ler(self):
        for contacto in GCdb().retornarDados()[0]:
            pass

    def labelContacto(self, _layout, _contacto):
        layout = QVBoxLayout()
        visualizador = QLabel()
        visualizador.setText(f"<b>Nome</b>: {_contacto[1]}<br>"
                             f"<b>Numero</b>: {_contacto[2]}<br>"
                             f"<b>Email</b>: {_contacto[3]}<br>"
                             f"<b>Morada</b>: {_contacto[4]}")

        prwBtn = QPushButton('')
        fecharBtn = QPushButton('')
        _layout.addRow(layout)

    def _novo(self):
        if not self.janelaNovoContacto:
            return self.novo()
        else:
            self.tab.setCurrentWidget(self.janelaNovoContacto)

    def novo(self):
        def atualizarIndicativo():
            self.indicativo = GCI().indicativo_especifico(comboPaises.currentText())
            self.numero.setPlaceholderText(f'+{self.indicativo}..')

        def validarEmail(_email):
            validador = re.compile(r'^[a-z0-9]+[._]?[a-z0-9]+[@]\w+[.]\w{2,3}')
            if validador.match(_email):
                return True
            return False

        def salvar():
            if (self.nome.text() or self.numero.text()) == '':
                QMessageBox.warning(self.ferramentas, 'Atenção', 'Contacto Não Guardado\n- Dados Obrigatórios Não Preenchidos..')
            elif not validarEmail(self.email.text()):
                QMessageBox.warning(self.ferramentas, 'Atenção', 'Contacto Não Guardado\n- Endereço de Email inválido..')
            else:
                nome = self.nome.text()
                email = self.email.text()
                numero = self.numero.text()
                morada = self.endereco.text()
                try:
                    GCdb().adicionarDados(nome, numero, email, morada)
                    QMessageBox.information(self.ferramentas, 'Concluido', 'Contacto Salvo com Sucesso..')
                    self.tab.removeTab(self.tab.currentIndex())
                except Exception as erro:
                    QMessageBox.critical(self.ferramentas, 'Falha', f'Ocorreu o Seguinte Erro Enquanto Processava a Operação: '
                                                                    f'\n- {erro}')

        self.janelaNovoContacto = QFrame()
        layout = QFormLayout()
        layout.setSpacing(20)

        iconLabel = QLabel()
        iconLabel.setPixmap(QPixmap('img/icons/user.png'))
        iconLabel.setAlignment(Qt.AlignRight)
        layout.addRow(iconLabel)

        self.nome = QLineEdit()
        self.nome.setPlaceholderText('Digite aqui o nome..')
        self.nome.setToolTip('Obrigatório')
        layout.addRow(self.nome)

        self.email = QLineEdit()
        self.email.setPlaceholderText('Digite aqui o email..')
        layout.addRow(self.email)

        paises = GCI().paises()
        comboPaises = QComboBox()
        comboPaises.addItems(paises)
        self.indicativo = GCI().indicativo_especifico(comboPaises.currentText())
        comboPaises.currentTextChanged.connect(atualizarIndicativo)

        self.numero = QLineEdit()
        self.numero.setPlaceholderText(f'+{self.indicativo}..')
        self.numero.setToolTip('Obrigatório')
        layout.addRow(comboPaises, self.numero)

        self.endereco = QLineEdit()
        self.endereco.setPlaceholderText('Digite aqui a morada..')
        self.endereco.setMaxLength(119)
        layout.addRow(self.endereco)

        btnSalvar = QPushButton('Salvar')
        btnSalvar.clicked.connect(salvar)
        layout.addWidget(btnSalvar)

        self.janelaNovoContacto.setLayout(layout)
        self.tab.addTab(self.janelaNovoContacto, 'Novo Contacto')
        self.tab.setCurrentWidget(self.janelaNovoContacto)

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
