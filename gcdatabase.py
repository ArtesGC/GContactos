import sqlite3
from os import makedirs


class GCdb:
    """classe para gerir as operacoes com a db"""

    def conectarDb(self):
        makedirs('Contactos', exist_ok=True)
        db = None
        try:
            db = sqlite3.connect('Contactos/gc.db')
            executor = db.cursor()
            resultado = executor.execute("CREATE TABLE IF NOT EXISTS gcontactos"
                                         "(id integer primary key autoincrement,"
                                         " nome varchar(80) not null,"
                                         " numero varchar(20) not null,"
                                         " email varchar(50),"
                                         " morada varchar(120));")
            if resultado:
                db.commit()
        except Exception:
            db = False
        return db

    def apagarDado(self, _nome):
        db = self.conectarDb()
        try:
            executor = db.cursor()
            resultado = executor.execute("DELETE FROM gcontactos WHERE nome=?", (_nome,))
            if resultado:
                db.commit()
                db.close()
                return True
        except Exception as erro:
            print(erro)
            return False
        if not db:
            raise ConnectionError(f'Erro ao conectar db!\nconnection_result:{db}')

    def adicionarDados(self, _nome, _numero, _email, _morada):
        db = self.conectarDb()
        try:
            executor = db.cursor()
            resultado = executor.execute('INSERT INTO gcontactos (nome, numero, email, morada) VALUES(?, ?, ?, ?);',
                                         (_nome, _numero, _email, _morada))
            if resultado:
                db.commit()
                db.close()
        except Exception as erro:
            print(erro)
        if not db:
            raise ConnectionError(f'Erro ao conectar db!\nconnection_result:{db}')
        return True

    def atualizarDados(self, _id, _nome, _numero, _email, _morada):
        db = self.conectarDb()
        try:
            executor = db.cursor()
            resultado = executor.execute("UPDATE gcontactos "
                                         "SET nome=?, numero=?, email=?, morada=?"
                                         "WHERE id=?", (_nome, _numero, _email, _morada, _id))
            if resultado:
                db.commit()
                db.close()
                return True
        except Exception as erro:
            print(erro)
            return False
        if not db:
            raise ConnectionError(f'Erro ao conectar db!\nconnection_result:{db}')

    def retornarDados(self, _nome=None):
        resultado = None
        db = self.conectarDb()
        try:
            executor = db.cursor()
            if _nome:
                resultado = executor.execute("SELECT * FROM gcontactos WHERE nome=?", (_nome,))
            else:
                resultado = executor.execute("SELECT * FROM gcontactos")
        except Exception as erro:
            print(erro)
            return False
        if not db:
            raise ConnectionError(f'Erro ao conectar db!\nconnection_result:{db}')
        elif resultado:
            dados = executor.fetchall()
            return dados
