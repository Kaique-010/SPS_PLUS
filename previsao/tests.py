from django.test import TestCase
from django.urls import reverse
from Entradas_Produtos.models import EntradaEstoque
from Saidas_Produtos.models import SaidasEstoque
from licencas.models import Empresas, Licencas, Filiais
from produto.models import Produtos, SaldoProduto
from Entidades.models import Entidades

class PrevisaoEstoqueTestCase(TestCase):

    def setUp(self):
        """
        Configuração inicial para os testes.
        Cria instâncias de dados fictícios para os modelos usados.
        """
        # Criação de uma licença fictícia
        self.licenca = Licencas.objects.create(lice_nome='Licença Teste')

        # Criação de uma empresa e filial fictícias
        self.empresa = Empresas.objects.create(empr_nome='Empresa Teste', licenca=self.licenca)
        self.filial = Filiais.objects.create(fili_nome='Filial Teste', empresa=self.empresa)

        # Criação de um produto fictício e salvar
        self.produto = Produtos.objects.create(prod_nome='Produto Teste', prod_codi='P001')

        # Criação de uma instância de Entidades
        self.entidade = Entidades.objects.create(enti_nome="Entidade Teste")

        # Criação de entradas, saídas e saldo de estoque fictícios, usando a instância de Entidades
        EntradaEstoque.objects.create(
            entr_prod=self.produto, 
            entr_empr=self.empresa, 
            entr_fili=self.filial, 
            entr_data='2025-02-01', 
            entr_quan=100, 
            entr_tota=100, 
            entr_enti=self.entidade
        )
        SaidasEstoque.objects.create(
            said_prod=self.produto, 
            said_empr=self.empresa, 
            said_fili=self.filial, 
            said_data='2025-02-02', 
            said_quan=50, 
            said_tota= 1, 
            said_enti=self.entidade
        )

        # Evitar duplicação ao inserir saldo
        if not SaldoProduto.objects.filter(sapr_prod=self.produto, sapr_empr=self.empresa, sapr_fili=self.filial).exists():
            SaldoProduto.objects.create(
                sapr_prod=self.produto, 
                sapr_empr=self.empresa, 
                sapr_fili=self.filial, 
                sapr_sald=200
            )

    def test_previsao_estoque(self):
        """
        Testa a view de previsão de estoque.
        """
        # Definir a URL da previsão de estoque
        url = reverse('previsao_estoque', kwargs={
            'produto': self.produto,
            'empresa_id': self.empresa.id,
            'filial_id': self.filial.id,
            'licenca_id': self.licenca.id,
        })

        # Realizar a requisição GET
        response = self.client.get(url)

        # Validar a resposta (verifica se o status é 200)
        self.assertEqual(response.status_code, 200)

        # Validar que as previsões estão no formato esperado
        data = response.json()
        self.assertIn('previsoes', data)  # Verifica se a chave 'previsoes' está no JSON de resposta
        self.assertGreater(len(data['previsoes']), 0)  # Verifica se existem previsões

    def test_sem_dados(self):
        """
        Testa o caso onde não há dados para previsão de estoque.
        """
        # Criar novos dados sem estoque, para testar a resposta com erro
        produto_sem_estoque = Produtos.objects.create(prod_nome='Produto Sem Estoque', prod_codi='P002')

        # Definir a URL para o produto sem estoque
        url = reverse('previsao_estoque', kwargs={
            'produto_id': produto_sem_estoque.id,
            'empresa_id': self.empresa.id,
            'filial_id': self.filial.id,
            'licenca_id': self.licenca.id,
        })

        # Realizar a requisição GET
        response = self.client.get(url)

        # Validar a resposta (deve retornar um erro porque não há dados)
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertEqual(data['error'], "Sem dados para previsão")
