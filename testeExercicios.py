# -*- coding: utf-8 -*-
"""Um teste identificado para cada exercício pedido na atividade."""

import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from grafoMatriz import Grafo, GrafoND, GrafoPonderado
from grafoLista import Grafo as GrafoLista
from grafoLista import GrafoND as GrafoNDLista


class TesteExercicios(unittest.TestCase):
    def dirigido_matriz(self):
        g = Grafo(5)
        for v, w in [(0, 1), (0, 2), (2, 1), (2, 3), (1, 3)]:
            g.insereA(v, w)
        return g

    def dirigido_lista(self):
        g = GrafoLista(5)
        for v, w in [(0, 1), (0, 2), (2, 1), (2, 3), (1, 3)]:
            g.insereA(v, w)
        return g

    def test_exercicio_01_in_degree_matriz(self):
        self.assertEqual(self.dirigido_matriz().inDegree(1), 2)

    def test_exercicio_02_out_degree_matriz(self):
        self.assertEqual(self.dirigido_matriz().outDegree(0), 2)

    def test_exercicio_03_degree_matriz(self):
        self.assertEqual(self.dirigido_matriz().degree(2), 3)

    def test_exercicio_04_fonte_matriz(self):
        g = self.dirigido_matriz()
        self.assertEqual(g.isSource(0), 1)
        self.assertEqual(g.isSource(1), 0)

    def test_exercicio_05_sorvedouro_matriz(self):
        g = self.dirigido_matriz()
        self.assertEqual(g.isSink(3), 1)
        self.assertEqual(g.isSink(2), 0)

    def test_exercicio_06_simetria_matriz(self):
        self.assertEqual(self.dirigido_matriz().isSymmetric(), 0)

    def test_exercicio_07_leitura_arquivo_matriz(self):
        conteudo = "6\n8\n0 1\n0 5\n1 0\n1 5\n2 4\n3 1\n4 3\n3 5\n"
        with tempfile.TemporaryDirectory() as pasta:
            arquivo = Path(pasta) / "grafo.txt"
            arquivo.write_text(conteudo, encoding="utf-8")
            g = Grafo.from_file(arquivo)
        self.assertEqual((g.n, g.m), (6, 8))

    def test_exercicio_08_grafo_nao_dirigido_e_show_matriz(self):
        g = GrafoND(3)
        g.insereA(0, 1)
        g.insereA(1, 2)
        g.removeA(0, 1)
        saida = io.StringIO()
        with redirect_stdout(saida):
            g.show()
        self.assertIn("n:", saida.getvalue())
        self.assertIn("fim da impressao", saida.getvalue())
        self.assertEqual(g.m, 1)

    def test_exercicio_09_degree_nao_dirigido_matriz(self):
        g = GrafoND(4)
        for v, w in [(0, 1), (0, 2), (1, 2), (2, 3)]:
            g.insereA(v, w)
        self.assertEqual(g.degree(2), 3)

    def test_exercicio_10_grafo_ponderado_matriz(self):
        g = GrafoPonderado(3)
        g.insereA(0, 1, 2.5)
        self.assertEqual(g.adj[0][1], 2.5)
        self.assertEqual(g.m, 1)

    def test_exercicio_11_remocao_vertice_matriz(self):
        g = Grafo(4)
        for v, w in [(0, 1), (1, 2), (2, 3), (3, 1)]:
            g.insereA(v, w)
        g.remove_vertex(1)
        self.assertEqual((g.n, g.m), (3, 1))
        nd = GrafoND(3)
        nd.insereA(0, 1)
        nd.insereA(1, 2)
        nd.remove_vertex(1)
        self.assertEqual((nd.n, nd.m), (2, 0))

    def test_exercicio_12_completo_nao_dirigido_matriz(self):
        g = GrafoND(3)
        for v, w in [(0, 1), (0, 2), (1, 2)]:
            g.insereA(v, w)
        self.assertEqual(g.isComplete(), 1)

    def test_exercicio_13_completo_dirigido_matriz(self):
        g = Grafo(3)
        for v, w in [(0, 1), (1, 0), (0, 2), (2, 0), (1, 2), (2, 1)]:
            g.insereA(v, w)
        self.assertEqual(g.isComplete(), 1)

    def test_exercicio_14_complemento_matriz(self):
        dirigido = Grafo(3)
        dirigido.insereA(0, 1)
        self.assertEqual(dirigido.complemento().m, 5)
        nao_dirigido = GrafoND(3)
        nao_dirigido.insereA(0, 1)
        self.assertEqual(nao_dirigido.complemento().m, 2)

    def test_exercicio_15_conexidade_nao_dirigida_matriz(self):
        g = GrafoND(3)
        g.insereA(0, 1)
        g.insereA(1, 2)
        self.assertEqual(g.connectivity_type(), 0)
        g.removeA(1, 2)
        self.assertEqual(g.connectivity_type(), 1)

    def test_exercicio_16_categoria_conexidade_matriz(self):
        forte = Grafo(3)
        for v, w in [(0, 1), (1, 2), (2, 0)]:
            forte.insereA(v, w)
        self.assertEqual(forte.categoria_conexidade(), 3)
        unilateral = Grafo(3)
        unilateral.insereA(0, 1)
        unilateral.insereA(1, 2)
        self.assertEqual(unilateral.categoria_conexidade(), 2)
        fraco = Grafo(3)
        fraco.insereA(0, 1)
        fraco.insereA(2, 1)
        self.assertEqual(fraco.categoria_conexidade(), 1)
        desconexo = Grafo(3)
        desconexo.insereA(0, 1)
        self.assertEqual(desconexo.categoria_conexidade(), 0)

    def test_exercicio_17_grafo_reduzido_matriz(self):
        g = Grafo(4)
        for v, w in [(0, 1), (1, 0), (1, 2), (2, 3)]:
            g.insereA(v, w)
        reduzido = g.grafo_reduzido()
        self.assertEqual((reduzido.n, reduzido.m), (3, 2))

    def test_exercicio_18_in_degree_lista(self):
        self.assertEqual(self.dirigido_lista().inDegree(1), 2)

    def test_exercicio_19_out_degree_lista(self):
        self.assertEqual(self.dirigido_lista().outDegree(0), 2)

    def test_exercicio_20_degree_lista(self):
        self.assertEqual(self.dirigido_lista().degree(2), 3)

    def test_exercicio_21_grafos_iguais_lista(self):
        g = self.dirigido_lista()
        h = GrafoLista(5)
        for v, w in reversed([(0, 1), (0, 2), (2, 1), (2, 3), (1, 3)]):
            h.insereA(v, w)
        self.assertEqual(g.equals(h), 1)

    def test_exercicio_22_conversao_lista_matriz(self):
        matriz = Grafo(4)
        for v, w in [(0, 1), (0, 3), (2, 1)]:
            matriz.insereA(v, w)
        lista = GrafoLista.from_matriz(matriz)
        matriz_convertida = lista.to_matriz()
        self.assertEqual(matriz_convertida.adj, matriz.adj)

    def test_exercicio_23_inversao_lista(self):
        g = self.dirigido_lista()
        antes = [lista[:] for lista in g.listaAdj]
        g.invert()
        self.assertEqual(g.listaAdj, [lista[::-1] for lista in antes])

    def test_exercicio_24_fonte_lista(self):
        self.assertEqual(self.dirigido_lista().isSource(0), 1)

    def test_exercicio_25_sorvedouro_lista(self):
        self.assertEqual(self.dirigido_lista().isSink(3), 1)

    def test_exercicio_26_simetria_lista(self):
        self.assertEqual(self.dirigido_lista().isSymmetric(), 0)

    def test_exercicio_27_leitura_arquivo_lista(self):
        conteudo = "4\n4\n0 1\n0 3\n2 1\n3 2\n"
        with tempfile.TemporaryDirectory() as pasta:
            arquivo = Path(pasta) / "grafo.txt"
            arquivo.write_text(conteudo, encoding="utf-8")
            g = GrafoLista.from_file(arquivo)
        self.assertEqual((g.n, g.m), (4, 4))

    def test_exercicio_28_remocao_vertice_nao_dirigido_lista(self):
        g = GrafoNDLista(4)
        for v, w in [(0, 1), (0, 2), (1, 2), (2, 3)]:
            g.insereA(v, w)
        g.remove_vertex(1)
        self.assertEqual((g.n, g.m), (3, 2))

    def test_exercicio_29_remocao_vertice_dirigido_lista(self):
        g = GrafoLista(4)
        for v, w in [(0, 1), (0, 3), (2, 1), (3, 2)]:
            g.insereA(v, w)
        g.remove_vertex(1)
        self.assertEqual((g.n, g.m), (3, 2))

    def test_exercicio_30_completo_lista(self):
        dirigido = GrafoLista(3)
        for v, w in [(0, 1), (1, 0), (0, 2), (2, 0), (1, 2), (2, 1)]:
            dirigido.insereA(v, w)
        self.assertEqual(dirigido.isComplete(), 1)
        nao_dirigido = GrafoNDLista(3)
        for v, w in [(0, 1), (0, 2), (1, 2)]:
            nao_dirigido.insereA(v, w)
        self.assertEqual(nao_dirigido.isComplete(), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
