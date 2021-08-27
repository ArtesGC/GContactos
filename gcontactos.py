import re
from sys import argv, exit
from PyQt5.Qt import *
from gcdatabase import GCdb
from gcindicativos import GCI

theme = open('themes/gcontactos.qss').read().strip()


class GContactos:
    def __init__(self):
        self.gc = QApplication(argv)

        self.fonteDB = QFontDatabase()
        self.fonteDB.addApplicationFont('fonts/laila.ttf')

        self.ferramentas = QWidget()
        self.ferramentas.setStyleSheet(theme)
        self.ferramentas.setFixedSize(600, 600)
        self.ferramentas.setWindowTitle('GContactos')
        self.ferramentas.setWindowIcon(QIcon("img/artesgc.png"))

        menu = QMenuBar(self.ferramentas)
        opcoes = menu.addMenu("Opções")

        home = opcoes.addAction(QIcon("img/icons/notebook.png"), 'Lista Contactos')
        home.triggered.connect(self._principal)

        opcoes.addSeparator()

        novo = opcoes.addAction(QIcon('img/icons/newcontact.png'), 'Novo Contacto')
        novo.triggered.connect(self._novo)

        opcoes.addSeparator()

        _sair = lambda: exit(0)
        sair = opcoes.addAction(QIcon("img/icons/rempage.png"), 'Fechar')
        sair.triggered.connect(_sair)

        sobre = menu.addAction('Sobre')
        sobre.triggered.connect(self._sobre)

        self.tab = QTabWidget(self.ferramentas)
        self.tab.setMovable(True)
        self.tab.setTabBarAutoHide(True)
        self.tab.setDocumentMode(True)
        self.tab.setGeometry(0, 40, 600, 560)

        self.nome = None
        self.email = None
        self.numero = None
        self.morada = None
        self.indicativo = None
        self.janelaNovoContacto = None
        self.janelaEditarContacto = None
        self.janelaListaContactos = None

        self.principal()

    def _principal(self):
        if not self.janelaListaContactos:
            return self.principal()
        elif self.janelaListaContactos.isHidden():
            self.janelaListaContactos.setHidden(False)
            self.tab.addTab(self.janelaListaContactos, 'Contactos')
            self.tab.setCurrentWidget(self.janelaListaContactos)
        else:
            self.tab.setCurrentWidget(self.janelaListaContactos)

    def atualizarListaContactos(self):
        self.tab.removeTab(self.tab.currentIndex())
        return self.principal()

    def principal(self):
        self.janelaListaContactos = QScrollArea()
        self.janelaListaContactos.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.janelaListaContactos.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.janelaListaContactos.setWidgetResizable(True)

        layout = QVBoxLayout()
        layout.setGeometry(QRect(0, 0, 500, 500))
        layout.setSpacing(10)

        iconLabel = QLabel()
        iconLabel.setPixmap(QPixmap('img/icons/contacts.png'))
        iconLabel.setAlignment(Qt.AlignRight)
        layout.addWidget(iconLabel)

        introLabel = QLabel('<h2>Lista de Contactos</h2>')
        introLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(introLabel)

        for contacto in GCdb().retornarDados():
            layout.addWidget(self.labelContacto(contacto))

        updtBtn = QPushButton('Atualizar')
        updtBtn.clicked.connect(self.atualizarListaContactos)
        layout.addWidget(updtBtn)

        self.janelaListaContactos.setLayout(layout)
        self.tab.addTab(self.janelaListaContactos, 'Contactos')
        self.tab.setCurrentWidget(self.janelaListaContactos)

    def _editar(self, nome=None):
        if not self.janelaEditarContacto:
            return self.editar(nome)
        elif self.janelaEditarContacto.isHidden():
            self.janelaEditarContacto.setHidden(False)
            return self.editar(nome)
        else:
            self.tab.setCurrentWidget(self.janelaEditarContacto)

    def editar(self, nome=None):
        def _fecharTab():
            self.tab.removeTab(self.tab.currentIndex())
            self.atualizarListaContactos()

        def atualizarIndicativo():
            self.indicativo = GCI().indicativo_especifico(comboPaises.currentText())
            self.numero.setText(f'(+{self.indicativo}){contacto[2]}')

        def salvar():
            if (self.nome.text() or self.numero.text()) == '':
                QMessageBox.warning(self.ferramentas, 'Atenção', 'Contacto Não Guardado\n- Dados Obrigatórios Não Preenchidos..')
            elif not validarEmail(self.email.text()):
                QMessageBox.warning(self.ferramentas, 'Atenção', 'Contacto Não Guardado\n- Endereço de Email inválido..')
            else:
                _id = contacto[0]
                _nome = self.nome.text()
                _email = self.email.text()
                _numero = self.numero.text()
                _morada = self.morada.text()
                try:
                    GCdb().atualizarDados(_id, _nome, _numero, _email, _morada)
                    QMessageBox.information(self.ferramentas, 'Concluido', 'Contacto Salvo com Sucesso..')
                    self.tab.removeTab(self.tab.currentIndex())
                except Exception as erro:
                    QMessageBox.critical(self.ferramentas, 'Falha', f'Ocorreu o Seguinte Erro Enquanto Processava a Operação: '
                                                                    f'\n- {erro}')

        self.janelaEditarContacto = QFrame()
        layout = QFormLayout()
        layout.setSpacing(10)

        iconLabel = QLabel()
        iconLabel.setPixmap(QPixmap('img/icons/editcontact.png'))
        iconLabel.setAlignment(Qt.AlignRight)
        layout.addRow(iconLabel)

        introLabel = QLabel('<h2>Editar Contacto</h2>')
        introLabel.setAlignment(Qt.AlignCenter)
        layout.addRow(introLabel)

        contacto = GCdb().retornarDados(nome)[0]

        self.nome = QLineEdit()
        self.nome.setPlaceholderText('Digite aqui o nome..')
        self.nome.setText(contacto[1])
        self.nome.setToolTip('Obrigatório')
        layout.addRow(self.nome)

        paises = GCI().paises()
        comboPaises = QComboBox()
        comboPaises.addItems(paises)
        self.indicativo = GCI().indicativo_especifico(comboPaises.currentText())
        comboPaises.currentTextChanged.connect(atualizarIndicativo)

        self.numero = QLineEdit()
        self.numero.setMaxLength(19)
        self.numero.setToolTip('Obrigatório')
        self.numero.setText(contacto[2])
        layout.addRow(comboPaises, self.numero)

        self.email = QLineEdit()
        self.email.setPlaceholderText('Digite aqui o email..')
        self.email.setText(contacto[3])
        layout.addRow(self.email)

        self.morada = QLineEdit()
        self.morada.setPlaceholderText('Digite aqui a morada..')
        self.morada.setMaxLength(119)
        self.morada.setText(contacto[4])
        layout.addRow(self.morada)

        btnSalvar = QPushButton('Salvar')
        btnSalvar.clicked.connect(salvar)
        layout.addWidget(btnSalvar)

        self.janelaEditarContacto.setLayout(layout)
        self.tab.addTab(self.janelaEditarContacto, 'Editar Contacto')
        self.tab.setCurrentWidget(self.janelaEditarContacto)
        self.tab.setTabToolTip(self.tab.currentIndex(), 'Dica: clique duas vezes para fechar a aba!')
        self.tab.tabBarDoubleClicked.connect(_fecharTab)

    def labelContacto(self, _contacto):
        def editar():
            self._editar(_contacto[1])

        def apagar():
            try:
                GCdb().apagarDado(_nome=_contacto[1])
                QMessageBox.information(self.ferramentas, 'Concluido', 'Operação bem-sucedida..')
                self.atualizarListaContactos()
            except Exception as erro:
                QMessageBox.warning(self.ferramentas, 'Aviso', f'Ocorreu o seguinte erro ao apagar o contacto:\n- {erro}')

        frame = QFrame()
        frame.setStyleSheet("QFrame{border-radius: 5px;"
                            "background-color: brown;"
                            "color: #EDB;"
                            "height: 200px}")

        layout = QFormLayout()
        layout.setSpacing(10)

        visualizador = QLabel()
        visualizador.setText(f"<b>Nome</b>: {_contacto[1]}<br>"
                             f"<b>Numero</b>: {_contacto[2]}<br>"
                             f"<b>Email</b>: {_contacto[3]}<br>"
                             f"<b>Morada</b>: {_contacto[4]}")
        iconVisualizador = QLabel()
        iconVisualizador.setPixmap(QPixmap('img/icons/user.png'))
        iconVisualizador.setStyleSheet("QLabel{background-color: #EDB;}")
        layout.addRow(iconVisualizador, visualizador)

        layoutBtns = QHBoxLayout()
        edtBtn = QPushButton(QIcon('img/icons/edit.png'), 'Editar Contacto')
        edtBtn.setStyleSheet("QPushButton{"
                             "background-color: #EDB;"
                             "color: black;"
                             "border-radius: 5px;"
                             "border-width: 1px;"
                             "border-style: solid;"
                             "border-color: black;"
                             "padding: 5px;}"
                             "QPushButton:hover{"
                             "background-color: white;"
                             "color: black;"
                             "border-radius: 5px;"
                             "border-width: 1px;"
                             "border-color: black;"
                             "border-style: solid;"
                             "padding: 5px;}")
        edtBtn.clicked.connect(editar)
        layoutBtns.addWidget(edtBtn)
        delBtn = QPushButton(QIcon('img/icons/delete.png'), 'Apagar Contacto')
        delBtn.setStyleSheet("QPushButton{"
                             "background-color: #EDB;"
                             "color: black;"
                             "border-radius: 5px;"
                             "border-width: 1px;"
                             "border-style: solid;"
                             "border-color: black;"
                             "padding: 5px;}"
                             "QPushButton:hover{"
                             "background-color: white;"
                             "color: black;"
                             "border-radius: 5px;"
                             "border-width: 1px;"
                             "border-color: black;"
                             "border-style: solid;"
                             "padding: 5px;}")
        delBtn.clicked.connect(apagar)
        layoutBtns.addWidget(delBtn)
        layout.addRow(layoutBtns)

        frame.setLayout(layout)
        return frame

    def _novo(self):
        if not self.janelaNovoContacto:
            return self.novo()
        elif self.janelaNovoContacto.isHidden():
            self.janelaNovoContacto.setHidden(False)
            self.tab.addTab(self.janelaNovoContacto, 'Novo Contacto')
            self.tab.setCurrentWidget(self.janelaNovoContacto)
        else:
            self.tab.setCurrentWidget(self.janelaNovoContacto)

    def novo(self):
        def _fecharTab():
            self.tab.removeTab(self.tab.currentIndex())
            self.atualizarListaContactos()

        def atualizarIndicativo():
            self.indicativo = GCI().indicativo_especifico(comboPaises.currentText())
            self.numero.setText(f'+{self.indicativo}')

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
                morada = self.morada.text()
                try:
                    GCdb().adicionarDados(nome, numero, email, morada)
                    QMessageBox.information(self.ferramentas, 'Concluido', 'Contacto Salvo com Sucesso..')
                    self.tab.removeTab(self.tab.currentIndex())
                except Exception as erro:
                    QMessageBox.critical(self.ferramentas, 'Falha', f'Ocorreu o Seguinte Erro Enquanto Processava a Operação: '
                                                                    f'\n- {erro}')

        self.janelaNovoContacto = QFrame()
        layout = QFormLayout()
        layout.setSpacing(10)

        iconLabel = QLabel()
        iconLabel.setPixmap(QPixmap('img/icons/newcontact.png'))
        iconLabel.setAlignment(Qt.AlignRight)
        layout.addRow(iconLabel)

        introLabel = QLabel('<h2>Novo Contacto</h2>')
        introLabel.setAlignment(Qt.AlignCenter)
        layout.addRow(introLabel)

        self.nome = QLineEdit()
        self.nome.setPlaceholderText('Digite aqui o nome..')
        self.nome.setToolTip('Obrigatório')
        layout.addRow(self.nome)

        paises = GCI().paises()
        comboPaises = QComboBox()
        comboPaises.addItems(paises)
        self.indicativo = GCI().indicativo_especifico(comboPaises.currentText())
        comboPaises.currentTextChanged.connect(atualizarIndicativo)

        self.numero = QLineEdit()
        self.numero.setText(f'+{self.indicativo}')
        self.numero.setMaxLength(19)
        self.numero.setToolTip('Obrigatório')
        layout.addRow(comboPaises, self.numero)

        self.email = QLineEdit()
        self.email.setPlaceholderText('Digite aqui o email..')
        layout.addRow(self.email)

        self.morada = QLineEdit()
        self.morada.setPlaceholderText('Digite aqui a morada, separada por virgulas..')
        self.morada.setMaxLength(119)
        layout.addRow(self.morada)

        btnSalvar = QPushButton('Salvar')
        btnSalvar.clicked.connect(salvar)
        layout.addWidget(btnSalvar)

        self.janelaNovoContacto.setLayout(layout)
        self.tab.addTab(self.janelaNovoContacto, 'Novo Contacto')
        self.tab.setCurrentWidget(self.janelaNovoContacto)
        self.tab.setTabToolTip(self.tab.currentIndex(), 'Dica: clique duas vezes para fechar a aba!')
        self.tab.tabBarDoubleClicked.connect(_fecharTab)

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
