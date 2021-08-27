import unittest
from gcdatabase import GCdb


class MyTestCase(unittest.TestCase):
    def test_conexaoDb(self):
        self.assertTrue(GCdb().conectarDb())

    def test_adicionardados(self):
        self.assertTrue(GCdb().adicionarDados(_nome='gc', _numero='12345',
                                              _morada='sa', _email='nurul@gmail.com'))

    def test_visualizardados(self):
        dados = GCdb().retornarDados(_nome='nurul')
        if dados:
            return True
        return False

    def test_atualizardados(self):
        self.assertTrue(GCdb().atualizarDados(_nome='nurul', _numero='54321',
                                              _morada='ao', _email='gc@gmail.com', _id=0))

    def test_apagardados(self):
        self.assertTrue(GCdb().apagarDado(_nome='nurul'))


if __name__ == '__main__':
    unittest.main()
