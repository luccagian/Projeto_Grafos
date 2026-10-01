# -*- coding: utf-8 -*-
"""
Integrantes:
Gabriel Medina - 10426931
Gian Lucca Campanha Ribeiro - 10438361
Lucas Carmo - 10439830

Arquivo: testeProjeto.py
Resumo: Testes das funções exigidas e as acrescentadas.
"""

import tempfile
import unittest
from pathlib import Path

from grafoMatriz import Grafo, GrafoND


class TesteProjeto(unittest.TestCase):

    def criar_grafo_nd_ponderado(self):
        g = GrafoND(
            3,
            ponderado=True,
            tipo_grafo=3,
            rotulos=["Sé", "República", "Luz"],
            pesos_vertices=[100.0, 80.0, 90.0],
        )
        g.insereA(0, 1, 2.0)
        g.insereA(1, 2, 3.0)
        return g

    def test_01_aresta_nao_dirigida_e_simetrica(self):
        g = self.criar_grafo_nd_ponderado()
        self.assertEqual(g.adj[0][1], 2.0)
        self.assertEqual(g.adj[1][0], 2.0)
        self.assertEqual(g.m, 2)

    def test_02_remocao_aresta_nao_dirigida(self):
        g = self.criar_grafo_nd_ponderado()
        g.removeA(0, 1)
        self.assertIsNone(g.adj[0][1])
        self.assertIsNone(g.adj[1][0])
        self.assertEqual(g.m, 1)

    def test_03_insercao_vertice_com_rotulo_e_peso(self):
        g = self.criar_grafo_nd_ponderado()
        indice = g.inserir_vertice("Brás", 70.0)
        self.assertEqual(indice, 3)
        self.assertEqual(g.rotulos[3], "Brás")
        self.assertEqual(g.pesos_vertices[3], 70.0)

    def test_04_remocao_vertice_remove_arestas(self):
        g = self.criar_grafo_nd_ponderado()
        g.remove_vertex(1)
        self.assertEqual(g.n, 2)
        self.assertEqual(g.m, 0)
        self.assertEqual(g.rotulos, ["Sé", "Luz"])

    def test_05_conexidade_nao_dirigida(self):
        g = self.criar_grafo_nd_ponderado()
        self.assertTrue(g.eh_conexo())
        g.removeA(1, 2)
        self.assertFalse(g.eh_conexo())

    def test_06_salvar_e_ler_formato(self):
        g = self.criar_grafo_nd_ponderado()

        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "grafo.txt"
            g.salvar_arquivo(caminho)
            carregado = Grafo.from_file(caminho)

        self.assertIsInstance(carregado, GrafoND)
        self.assertEqual(carregado.tipo_grafo, 3)
        self.assertEqual(carregado.n, 3)
        self.assertEqual(carregado.m, 2)
        self.assertEqual(carregado.rotulos, ["Sé", "República", "Luz"])
        self.assertEqual(carregado.pesos_vertices, [100.0, 80.0, 90.0])
        self.assertEqual(carregado.adj[1][2], 3.0)

    def test_07_arquivo_nao_dirigido_nao_aceita_duplicacao_de_aresta(self):
        conteudo = """3
2
0 "A" 1
1 "B" 1
2
0 1 2
1 0 2
"""
        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "grafo.txt"
            caminho.write_text(conteudo, encoding="utf-8")
            with self.assertRaises(ValueError):
                Grafo.from_file(caminho)

    def test_08_grafo_dirigido_mantem_categoria_e_reduzido(self):
        g = Grafo(4)
        for v, w in [(0, 1), (1, 0), (1, 2), (2, 3)]:
            g.insereA(v, w)
        self.assertEqual(g.grafo_reduzido().n, 3)

    def test_09_dijkstra_encontra_menor_distancia(self):
        g = GrafoND(4, ponderado=True, tipo_grafo=2, rotulos=["A", "B", "C", "D"])
        g.insereA(0, 1, 2.0)
        g.insereA(1, 3, 2.0)
        g.insereA(0, 2, 1.0)
        g.insereA(2, 3, 10.0)
        distancia, caminho = g.caminho_minimo(0, 3)
        self.assertEqual(distancia, 4.0)
        self.assertEqual(caminho, [0, 1, 3])

    def test_10_dijkstra_aceita_integracao_com_peso_zero(self):
        g = GrafoND(3, ponderado=True, tipo_grafo=2, rotulos=["A", "A | Linha 2", "B"])
        g.insereA(0, 1, 0.0)
        g.insereA(1, 2, 1.5)
        distancia, caminho = g.caminho_minimo(0, 2)
        self.assertEqual(distancia, 1.5)
        self.assertEqual(caminho, [0, 1, 2])

    def test_11_simulacao_falha_nao_altera_grafo(self):
        g = GrafoND(3, ponderado=True, tipo_grafo=2, rotulos=["A | Linha 1", "B | Linha 1", "C | Linha 1"])
        g.insereA(0, 1, 1.0)
        g.insereA(1, 2, 1.0)
        resultado = g.simular_falha_estacao(1)
        self.assertFalse(resultado["continua_conexo"])
        self.assertTrue(resultado["falha_critica"])
        self.assertEqual(g.n, 3)
        self.assertEqual(g.m, 2)

    def test_12_falha_remove_todas_ocorrencias_da_estacao(self):
        g = GrafoND(4, ponderado=True, tipo_grafo=2, rotulos=[
            "Sé | Linha 1-Azul", "Sé | Linha 3-Vermelha", "A | Linha 1", "B | Linha 3"
        ])
        g.insereA(0, 1, 0.0)
        g.insereA(0, 2, 1.0)
        g.insereA(1, 3, 1.0)
        resultado = g.simular_falha_estacao(0)
        self.assertEqual(resultado["vertices_indisponiveis"], [0, 1])
        self.assertEqual(len(resultado["componentes_depois"]), 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
