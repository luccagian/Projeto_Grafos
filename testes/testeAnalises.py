"""
Integrantes:
Gabriel Medina - 10426931
Gian Lucca Campanha Ribeiro - 10438361
Lucas Carmo - 10439830

Arquivo: testeAnalises.py
Resumo: testes das análises da Parte 3 (resiliência e características do
        grafo), com grafos pequenos de resultado conhecido e conferência
        no grafo real da rede (dados/grafo.txt).

Histórico de alterações:
    2026-11-19 | Gabriel Medina | Criação dos testes das análises da Parte 3.
"""

import contextlib
import io
import unittest
from pathlib import Path
from unittest import mock

from grafos import analises
from grafos.grafoMatriz import Grafo, GrafoND
from interface import acoes_menu as acoes

ARQUIVO_REDE = Path(__file__).resolve().parent.parent / "dados" / "grafo.txt"


def criar_grafo(n, arestas, rotulos=None):
    """Cria um grafo não orientado ponderado (tipo 2) a partir de (v, w, peso)."""
    g = GrafoND(n, ponderado=True, tipo_grafo=2, rotulos=rotulos)
    for v, w, peso in arestas:
        g.insereA(v, w, peso)
    return g


class TesteResiliencia(unittest.TestCase):

    def test_01_articulacoes_e_pontes_em_triangulo_com_cauda(self):
        # Triângulo 0-1-2 com cauda 2-3-4: os vértices 2 e 3 separam a rede
        # e as arestas da cauda são pontes.
        g = criar_grafo(5, [(0, 1, 1), (1, 2, 1), (0, 2, 1), (2, 3, 1), (3, 4, 1)])
        articulacoes, pontes = analises.pontos_articulacao_e_pontes(g)
        self.assertEqual(articulacoes, [2, 3])
        self.assertEqual(pontes, [(2, 3), (3, 4)])

    def test_02_ciclo_nao_tem_articulacao_nem_ponte(self):
        g = criar_grafo(4, [(0, 1, 1), (1, 2, 1), (2, 3, 1), (3, 0, 1)])
        self.assertEqual(analises.pontos_articulacao_e_pontes(g), ([], []))

    def test_03_raiz_com_dois_filhos_e_articulacao(self):
        g = criar_grafo(3, [(0, 1, 1), (0, 2, 1)])
        articulacoes, pontes = analises.pontos_articulacao_e_pontes(g)
        self.assertEqual(articulacoes, [0])
        self.assertEqual(pontes, [(0, 1), (0, 2)])

    def test_04_grafo_desconexo_analisa_todas_as_componentes(self):
        g = criar_grafo(6, [(0, 1, 1), (1, 2, 1), (3, 4, 1), (4, 5, 1)])
        articulacoes, pontes = analises.pontos_articulacao_e_pontes(g)
        self.assertEqual(articulacoes, [1, 4])
        self.assertEqual(len(pontes), 4)

    def test_05_ranking_considera_todas_as_linhas_da_estacao(self):
        g = criar_grafo(5, [(0, 1, 0), (0, 2, 1), (1, 3, 1), (2, 4, 1)], rotulos=[
            "Centro | Linha 1", "Centro | Linha 2",
            "A | Linha 1", "B | Linha 2", "C | Linha 1"])
        ranking = analises.ranking_falhas_estacoes(g)
        centro = next(r for r in ranking if r["estacao"] == "Centro")
        self.assertEqual(centro["vertices"], [0, 1])
        self.assertEqual(centro["componentes"], 2)  # {A, C} e {B}
        self.assertEqual(centro["desconectados"], 1)
        self.assertTrue(centro["critica"])

    def test_06_rota_alternativa_com_desvio(self):
        # Losango: 0-1-2 (1+1) e 0-3-2 (2+2). Falha em 1 força o desvio por 3.
        g = criar_grafo(4, [(0, 1, 1), (1, 2, 1), (0, 3, 2), (3, 2, 2)],
                        rotulos=["O | L1", "X | L1", "D | L1", "Y | L2"])
        r = analises.rota_alternativa(g, 0, 2, 1)
        self.assertEqual(r["distancia_original"], 2)
        self.assertEqual(r["caminho_original"], [0, 1, 2])
        self.assertEqual(r["distancia_alternativa"], 4)
        self.assertEqual(r["caminho_alternativo"], [0, 3, 2])

    def test_07_rota_alternativa_inexistente_quando_falha_desconecta(self):
        g = criar_grafo(3, [(0, 1, 1), (1, 2, 1)], rotulos=["O | L1", "X | L1", "D | L1"])
        r = analises.rota_alternativa(g, 0, 2, 1)
        self.assertIsNone(r["distancia_alternativa"])
        self.assertEqual(r["caminho_alternativo"], [])

    def test_08_rota_alternativa_rejeita_origem_indisponivel(self):
        g = criar_grafo(3, [(0, 1, 1), (1, 2, 1)], rotulos=["O | L1", "X | L1", "D | L1"])
        with self.assertRaises(ValueError):
            analises.rota_alternativa(g, 1, 2, 1)


class TesteCaracteristicas(unittest.TestCase):

    def test_09_estatisticas_de_graus(self):
        g = criar_grafo(4, [(0, 1, 1), (0, 2, 1), (0, 3, 1)])
        graus = analises.estatisticas_graus(g)
        self.assertEqual(graus["minimo"], 1)
        self.assertEqual(graus["maximo"], 3)
        self.assertAlmostEqual(graus["media"], 1.5)
        self.assertEqual(graus["maior_grau"], [0])
        self.assertEqual(graus["distribuicao"], {1: 3, 3: 1})

    def test_10_euler_ciclo_percurso_e_nenhum(self):
        ciclo = criar_grafo(4, [(0, 1, 1), (1, 2, 1), (2, 3, 1), (3, 0, 1)])
        percurso = criar_grafo(3, [(0, 1, 1), (1, 2, 1)])
        estrela = criar_grafo(4, [(0, 1, 1), (0, 2, 1), (0, 3, 1)])
        self.assertEqual(analises.analise_euleriana(ciclo)["tipo"], "ciclo")
        self.assertEqual(analises.analise_euleriana(percurso)["tipo"], "percurso")
        self.assertEqual(analises.analise_euleriana(estrela)["tipo"], "nenhum")

    def test_11_euler_exige_grafo_conexo(self):
        g = criar_grafo(6, [(0, 1, 1), (1, 2, 1), (2, 0, 1), (3, 4, 1), (4, 5, 1), (5, 3, 1)])
        self.assertEqual(analises.analise_euleriana(g)["tipo"], "nenhum")

    def test_12_bipartido_e_coloracao_do_ciclo_par(self):
        g = criar_grafo(4, [(0, 1, 1), (1, 2, 1), (2, 3, 1), (3, 0, 1)])
        self.assertTrue(analises.eh_bipartido(g))
        self.assertEqual(analises.coloracao_welsh_powell(g)[0], 2)

    def test_13_triangulo_nao_e_bipartido_e_precisa_de_tres_cores(self):
        g = criar_grafo(3, [(0, 1, 1), (1, 2, 1), (2, 0, 1)])
        self.assertFalse(analises.eh_bipartido(g))
        self.assertEqual(analises.coloracao_welsh_powell(g)[0], 3)
        self.assertEqual(analises.clique_maxima(g)[0], 3)

    def test_14_coloracao_e_propria(self):
        g = criar_grafo(5, [(0, 1, 1), (1, 2, 1), (2, 0, 1), (2, 3, 1), (3, 4, 1)])
        _, cores = analises.coloracao_welsh_powell(g)
        for v in range(g.n):
            for w in range(g.n):
                if g._tem_aresta(v, w):
                    self.assertNotEqual(cores[v], cores[w])

    def test_15_hamilton_ciclo_descartado_por_grau_e_articulacao(self):
        g = criar_grafo(3, [(0, 1, 1), (1, 2, 1)])
        resultado = analises.condicoes_hamiltoniano(g)
        self.assertEqual(resultado["ciclo"], "não admite")
        self.assertEqual(resultado["caminho"], "inconclusivo")

    def test_16_hamilton_caminho_descartado_por_tres_folhas(self):
        g = criar_grafo(4, [(0, 1, 1), (0, 2, 1), (0, 3, 1)])
        resultado = analises.condicoes_hamiltoniano(g)
        self.assertEqual(resultado["caminho"], "não admite")

    def test_17_hamilton_ciclo_inconclusivo_em_ciclo_simples(self):
        g = criar_grafo(4, [(0, 1, 1), (1, 2, 1), (2, 3, 1), (3, 0, 1)])
        self.assertEqual(analises.condicoes_hamiltoniano(g)["ciclo"], "inconclusivo")

    def test_18_arvore_geradora_minima_kruskal(self):
        g = criar_grafo(4, [(0, 1, 1), (1, 2, 2), (0, 2, 3), (2, 3, 4), (1, 3, 9)])
        total, arvore, peso_grafo = analises.arvore_geradora_minima(g)
        self.assertEqual(total, 7)
        self.assertEqual(len(arvore), 3)
        self.assertEqual(peso_grafo, 19)

    def test_19_diametro_e_raio_de_caminho_ponderado(self):
        g = criar_grafo(4, [(0, 1, 1), (1, 2, 2), (2, 3, 3)])
        medidas = analises.diametro_e_raio(g)
        self.assertEqual(medidas["diametro"], 6)
        self.assertEqual(set(medidas["extremos"]), {0, 3})
        self.assertEqual(medidas["raio"], 3)
        self.assertEqual(medidas["centro"], 2)

    def test_20_grafo_orientado_e_rejeitado_pelas_acoes(self):
        with self.assertRaises(ValueError):
            acoes.analisar_caracteristicas(Grafo(3))
        with self.assertRaises(ValueError):
            acoes.investigar_resiliencia(Grafo(3))


class TesteRedeReal(unittest.TestCase):
    """Confere as análises no grafo do estudo de caso (203 vértices, 230 arestas)."""

    @classmethod
    def setUpClass(cls):
        cls.g = Grafo.from_file(ARQUIVO_REDE)

    def test_21_articulacoes_conferem_com_remocao_por_forca_bruta(self):
        lista = analises.lista_de_adjacencia(self.g)
        base = len(analises.componentes(lista))
        esperado = [
            v for v in range(self.g.n)
            if len(analises.componentes(lista, frozenset([v]))) > base
        ]
        articulacoes, _ = analises.pontos_articulacao_e_pontes(self.g)
        self.assertEqual(articulacoes, esperado)
        self.assertEqual(len(articulacoes), 95)

    def test_22_pontes_conferem_com_remocao_por_forca_bruta(self):
        copia = Grafo.from_file(ARQUIVO_REDE)
        base = len(copia.componentes_conexas())
        esperado = []
        for v in range(copia.n):
            for w in range(v + 1, copia.n):
                if copia._tem_aresta(v, w):
                    peso = copia.adj[v][w]
                    copia.removeA(v, w)
                    if len(copia.componentes_conexas()) > base:
                        esperado.append((v, w))
                    copia.insereA(v, w, peso)
        _, pontes = analises.pontos_articulacao_e_pontes(self.g)
        self.assertEqual(pontes, esperado)
        self.assertEqual(len(pontes), 95)

    def test_23_ranking_concorda_com_simulacao_de_falha(self):
        ranking = {r["estacao"]: r for r in analises.ranking_falhas_estacoes(self.g)}
        for vertice, nome in [(54, "Palmeiras-Barra Funda"), (12, "Sé"), (47, "Brás")]:
            simulacao = self.g.simular_falha_estacao(vertice)
            self.assertEqual(ranking[nome]["componentes"], len(simulacao["componentes_depois"]))
        self.assertEqual(ranking["Palmeiras-Barra Funda"]["componentes"], 3)
        self.assertFalse(ranking["Sé"]["critica"])

    def test_24_caracteristicas_da_rede(self):
        graus = analises.estatisticas_graus(self.g)
        self.assertEqual((graus["minimo"], graus["maximo"]), (1, 6))
        self.assertEqual(len(analises.analise_euleriana(self.g)["vertices_grau_impar"]), 46)
        self.assertEqual(analises.analise_euleriana(self.g)["tipo"], "nenhum")
        cores, _ = analises.coloracao_welsh_powell(self.g)
        self.assertEqual(cores, analises.clique_maxima(self.g)[0])
        self.assertEqual(cores, 5)
        self.assertFalse(analises.eh_bipartido(self.g))
        ham = analises.condicoes_hamiltoniano(self.g)
        self.assertEqual((ham["ciclo"], ham["caminho"]), ("não admite", "não admite"))
        total, arvore, _ = analises.arvore_geradora_minima(self.g)
        self.assertEqual(len(arvore), self.g.n - 1)
        self.assertAlmostEqual(total, 315.072, places=3)
        self.assertAlmostEqual(analises.diametro_e_raio(self.g)["diametro"], 104.551, places=3)

    def test_25_rota_alternativa_sem_a_se_acrescenta_distancia(self):
        r = analises.rota_alternativa(self.g, 6, 22, 12)  # Vila Mariana -> Tucuruvi sem Sé
        self.assertAlmostEqual(r["distancia_original"], 13.482, places=3)
        self.assertGreater(r["distancia_alternativa"], r["distancia_original"])

    def test_26_analises_nao_alteram_o_grafo(self):
        copia = Grafo.from_file(ARQUIVO_REDE)
        n, m, matriz = copia.n, copia.m, [linha[:] for linha in copia.adj]
        analises.pontos_articulacao_e_pontes(copia)
        analises.ranking_falhas_estacoes(copia)
        analises.arvore_geradora_minima(copia)
        analises.diametro_e_raio(copia)
        self.assertEqual((copia.n, copia.m, copia.adj), (n, m, matriz))

    def test_27_menu_exibe_as_analises(self):
        saida = io.StringIO()
        with contextlib.redirect_stdout(saida):
            acoes.analisar_caracteristicas(self.g)
            with mock.patch("builtins.input", side_effect=["1", "2", "3", "0"]):
                acoes.investigar_resiliencia(self.g)
        texto = saida.getvalue()
        for trecho in ("Características do grafo", "Welsh-Powell", "Kruskal",
                       "pontos de articulação", "pontes", "Ranking de estações"):
            self.assertIn(trecho, texto)


if __name__ == "__main__":
    unittest.main(verbosity=2)
