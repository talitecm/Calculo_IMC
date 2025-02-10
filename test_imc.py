import unittest
from app import app

class TestIMC(unittest.TestCase):
    # Configuração do teste
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    # Testa a página inicial (formulário)
    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Informe seu nome:', response.data)
        self.assertIn('Informe seu peso:', response.data)
        self.assertIn('Informe sua altura:', response.data)

    # Testa o cálculo do IMC com valores válidos
    def test_calcular_imc_valido(self):
        response = self.app.get('/resultado?nome=Joao&peso=70&altura=1.75')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Você está com o peso normal!', response.data)  # IMC esperado entre 18.5 e 24.9

    # Testa o cálculo do IMC com valores inválidos (peso não numérico)
    def test_calcular_imc_valores_invalidos_peso(self):
        response = self.app.get('/resultado?nome=Joao&peso=abc&altura=1.75')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Valores inválidos! Insira números válidos para peso e altura.', response.data)

    # Testa o cálculo do IMC com valores inválidos (altura não numérica)
    def test_calcular_imc_valores_invalidos_altura(self):
        response = self.app.get('/resultado?nome=Joao&peso=70&altura=abc')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Valores inválidos! Insira números válidos para peso e altura.', response.data)

    # Testa o caso quando os campos estão vazios
    def test_campos_vazios(self):
        response = self.app.get('/resultado?nome=&peso=&altura=')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Preencha todos os campos corretamente!', response.data)

    # Testa o cálculo do IMC com valor baixo (abaixo do peso)
    def test_imc_abaixo_peso(self):
        response = self.app.get('/resultado?nome=Joao&peso=50&altura=1.75')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Você está abaixo do peso!', response.data)

    # Testa o cálculo do IMC com sobrepeso
    def test_imc_sobrepeso(self):
        response = self.app.get('/resultado?nome=Joao&peso=90&altura=1.75')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Você está com sobrepeso!', response.data)

    # Testa o cálculo do IMC com obesidade
    def test_imc_obesidade(self):
        response = self.app.get('/resultado?nome=Joao&peso=120&altura=1.75')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Você está obeso!', response.data)

if __name__ == '__main__':
    unittest.main()