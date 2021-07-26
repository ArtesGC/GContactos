import sqlite3


class GCdb:
    """classe para gerir as operacoes com a db"""

    def criarDb(self):
        makedirs('Contactos', exist_ok=True)
        try:
            db = sqlite3.connect('Contactos/gc.db')
            executor = db.cursor()
            resultado = executor.execute("CREATE TABLE IF NOT EXISTS gcontactos"
                                         "(id integer primary key autoincrement,"
                                         " nome varchar(80) not null,"
                                         " numero varchar(20) not null,"
                                         " email varchar(50) not null,"
                                         " morada varchar(120) not null);")
            return executor
        except Exception as erro:
            print(f'[X]-{erro}')

    def apagarDados(self, _id):
        pass

    def adicionarDados(self, _nome, _numero, _email, _morada):
        executor = self.criarDb()
        try:
            result = executor.execute(f'INSERT INTO gcontactos '
                                      f'(nome, numero, email, morada) '
                                      f'VALUES("{_nome}","{_numero}","{_email}","{_morada}");')
            if result:
                executor.close()
                return True
        except Exception:
            executor.close()
            return False
