import unittest
from gcdatabase import GCdb


class MyTestCase(unittest.TestCase):
    def test_criacaoDb(self):
        self.assertTrue(GCdb().criarDb())

    def test_apagardados(self):
        self.assertTrue(GCdb().apagarDados(_id=1))

    def test_adicionardados(self):
        self.assertTrue(GCdb().adicionarDados(_nome='gc', _numero='12345',
                                              _morada='sa', _email='nurul@gmail.com'))


if __name__ == '__main__':
    unittest.main()
