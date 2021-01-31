# ************************************************
#  (c) 2019-2021 Nurul-GC                        *
# ************************************************

from os import makedirs, path
from PyQt5.Qt import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import notify2 as notify
from sys import argv


class L4C8:
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

        labelIntro = QLabel("<h2>'Nunca Confundas Talento Com Sorte!'<br> - GC</h2>")
        labelIntro.setAlignment(Qt.AlignCenter)
        labelIntro.setFont(QFont('cambria', italic=True))
        layout.addWidget(labelIntro)

        self.nome = QLineEdit()
        self.nome.setToolTip('OBRIGATÓRIO!')
        layout.addRow('&Nome: *', self.nome)

        self.numero = QLineEdit()
        self.numero.setToolTip('OBRIGATÓRIO!')
        layout.addRow('&Numero: *', self.numero)

        layoutEndereco = QVBoxLayout()
        self.endereco1 = QLineEdit()
        self.endereco2 = QLineEdit()
        layoutEndereco.addWidget(self.endereco1)
        layoutEndereco.addWidget(self.endereco2)
        layout.addRow('Endereço:', layoutEndereco)

        self.email = QLineEdit()
        layout.addRow('Email:', self.email)

        janela1.setLayout(layout)
        self.tab.addTab(janela1, 'Principal')
        self.tab.setCurrentWidget(janela1)

    def guardar_(self):
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
        elif (self.nome.text() and self.numero.text()) is '':
            QMessageBox.warning(self.ferramentas, 'Atenção', 'Contacto Não Guardado\n- Nome e Número Não Preenchidos..')
        else:
            if not path.exists('GContactos'):
                makedirs('GContactos')
            with open(f"GContactos/{self.nome.text()}.gcontact", 'w+') as file:
                if self.endereco1.text() == '' and self.endereco2.text() == '' and self.email.text() == '':
                    file.write(f'''Nome: {self.nome.get()}
Numero: {self.numero.get()}''')
                else:
                    file.write(f'''Nome: {self.nome.get()}
Numero: {self.numero.get()}
Morada: {self.morada1.get()}, {self.morada2.get()}
Email: {self.email.get()}''')
            self.guardar_()
            showinfo('Confirmação', 'Contacto Guardado\n 👌 👍')

    def editar_(self):
        if self.janela2 is None:
            return self.editar()
        try:
            self.tab.removeTab(1)
            return self.editar()
        except TclError:
            return self.editar()

    def editar(self):
        pass

    def ler(self):
        pass

    def sobre(self):
        QMessageBox.information(self.ferramentas, 'Sobre o Programa', f"""
Nome: ListaContactos GC
Versão: 0.6-012021
Designer e Programador: Nurul GC
Empresa: ArtesGC Inc.""")


if __name__ == '__main__':
    try:
        app = L4C8()
        app.ferramentas.show()
        app.gc.exec_()
    except Exception as erro:
        notify.init(app_name='lista_contactos_gc')
        notificao = notify.Notification(summary='Falha', message=f'Ocorreu um erro ao iniciar a aplicação..')
        notificao.show()
