# -*- coding: utf-8 -*-
"""
Integrantes:
Gabriel Medina - 10426931
Gian Lucca Campanha Ribeiro - 10438361
Lucas Carmo - 10439830

Arquivo: grafoMatriz.py
Resumo: implementação do grafo por matriz de adjacência usada no projeto.
"""

from __future__ import annotations

from collections import deque
from pathlib import Path
import heapq
import math
import shlex
from typing import Iterable


TIPOS_GRAFO = {
    0: (False, False, False),  # não orientado, sem pesos
    1: (False, True,  False),  # não orientado, peso no vértice
    2: (False, False, True),   # não orientado, peso na aresta
    3: (False, True,  True),   # não orientado, peso no vértice e na aresta
    4: (True,  False, False),  # orientado, sem pesos
    5: (True,  True,  False),  # orientado, peso no vértice
    6: (True,  False, True),   # orientado, peso na aresta
    7: (True,  True,  True),   # orientado, peso no vértice e na aresta
}


class Grafo:
    """Grafo dirigido representado por matriz de adjacência."""

    TAM_MAX_DEFAULT = 100

    def __init__(
        self,
        n: int = TAM_MAX_DEFAULT,
        ponderado: bool = False,
        *,
        tipo_grafo: int | None = None,
        rotulos: Iterable[str] | None = None,
        pesos_vertices: Iterable[float | None] | None = None,
    ) -> None:
        if not isinstance(n, int) or n < 0:
            raise ValueError("A quantidade de vértices deve ser um inteiro não negativo.")

        if tipo_grafo is None:
            tipo_grafo = 6 if ponderado else 4
        self._validar_tipo(tipo_grafo)

        direcionado, peso_vertice, peso_aresta = TIPOS_GRAFO[tipo_grafo]
        if not direcionado:
            raise ValueError(
                "A classe Grafo representa grafos orientados. "
                "Use GrafoND para tipos 0 a 3."
            )

        self.tipo_grafo = tipo_grafo
        self.n = n
        self.m = 0
        self.ponderado = peso_aresta
        self.tem_peso_vertice = peso_vertice

        vazio = None if self.ponderado else 0
        self.adj = [[vazio for _ in range(n)] for _ in range(n)]

        self.rotulos = list(rotulos) if rotulos is not None else [str(i) for i in range(n)]
        self.pesos_vertices = (
            list(pesos_vertices)
            if pesos_vertices is not None
            else [None for _ in range(n)]
        )
        self._validar_metadados_vertices()

    # \1

    @staticmethod
    def _validar_tipo(tipo_grafo: int) -> None:
        if tipo_grafo not in TIPOS_GRAFO:
            raise ValueError("Tipo do grafo deve estar entre 0 e 7.")

    @property
    def direcionado(self) -> bool:
        return TIPOS_GRAFO[self.tipo_grafo][0]

    @property
    def peso_no_vertice(self) -> bool:
        return TIPOS_GRAFO[self.tipo_grafo][1]

    @property
    def peso_na_aresta(self) -> bool:
        return TIPOS_GRAFO[self.tipo_grafo][2]

    def _validar_metadados_vertices(self) -> None:
        if len(self.rotulos) != self.n:
            raise ValueError("A quantidade de rótulos deve ser igual a n.")
        if len(self.pesos_vertices) != self.n:
            raise ValueError("A quantidade de pesos de vértice deve ser igual a n.")

    def _validar_vertice(self, v: int) -> None:
        if not isinstance(v, int) or not 0 <= v < self.n:
            raise IndexError(f"Vértice inválido: {v}")

    def _tem_aresta(self, v: int, w: int) -> bool:
        return self.adj[v][w] is not None if self.ponderado else self.adj[v][w] != 0

    # \1

    def insereA(self, v: int, w: int, peso: float | None = None) -> None:
        self._validar_vertice(v)
        self._validar_vertice(w)

        if self._tem_aresta(v, w):
            return

        if self.ponderado:
            if peso is None:
                raise ValueError("Este grafo exige peso na aresta.")
            valor = float(peso)
        else:
            valor = 1

        self.adj[v][w] = valor
        self.m += 1

    def removeA(self, v: int, w: int) -> None:
        self._validar_vertice(v)
        self._validar_vertice(w)

        if not self._tem_aresta(v, w):
            return

        self.adj[v][w] = None if self.ponderado else 0
        self.m -= 1

    def inserir_vertice(self, rotulo: str, peso: float | None = None) -> int:
        """Insere um vértice e retorna seu índice."""
        rotulo = str(rotulo).strip()
        if not rotulo:
            raise ValueError("O rótulo do vértice não pode ser vazio.")

        if self.peso_no_vertice and peso is None:
            raise ValueError("Este tipo de grafo exige peso no vértice.")
        if not self.peso_no_vertice:
            peso = None

        vazio = None if self.ponderado else 0
        for linha in self.adj:
            linha.append(vazio)
        self.n += 1
        self.adj.append([vazio for _ in range(self.n)])

        self.rotulos.append(rotulo)
        self.pesos_vertices.append(None if peso is None else float(peso))
        return self.n - 1

    def remove_vertex(self, v: int) -> None:
        self._validar_vertice(v)

        self.adj.pop(v)
        for linha in self.adj:
            linha.pop(v)

        self.rotulos.pop(v)
        self.pesos_vertices.pop(v)
        self.n -= 1

        self.m = sum(
            1
            for i in range(self.n)
            for j in range(self.n)
            if self._tem_aresta(i, j)
        )

    removeV = remove_vertex
    removeVertice = remove_vertex

    # \1

    def inDegree(self, v: int) -> int:
        self._validar_vertice(v)
        return sum(1 for u in range(self.n) if self._tem_aresta(u, v))

    def outDegree(self, v: int) -> int:
        self._validar_vertice(v)
        return sum(1 for w in range(self.n) if self._tem_aresta(v, w))

    def degree(self, v: int) -> int:
        return self.inDegree(v) + self.outDegree(v)

    def isSource(self, v: int) -> int:
        return int(self.outDegree(v) > 0 and self.inDegree(v) == 0)

    def isSink(self, v: int) -> int:
        return int(self.inDegree(v) > 0 and self.outDegree(v) == 0)

    fonte = isSource
    sorvedouro = isSink

    def isSymmetric(self) -> int:
        return int(
            all(
                self._tem_aresta(i, j) == self._tem_aresta(j, i)
                for i in range(self.n)
                for j in range(self.n)
            )
        )

    simetrico = isSymmetric

    def isComplete(self) -> int:
        return int(
            all(
                i == j or self._tem_aresta(i, j)
                for i in range(self.n)
                for j in range(self.n)
            )
        )

    completo = isComplete

    def complemento(self) -> "Grafo":
        resultado = Grafo(self.n, tipo_grafo=4)
        for i in range(self.n):
            for j in range(self.n):
                if i != j and not self._tem_aresta(i, j):
                    resultado.insereA(i, j)
        return resultado

    complement = complemento

    # \1

    def caminho_minimo(
        self,
        origem: int,
        destino: int,
        ignorar_vertices: Iterable[int] | None = None,
    ) -> tuple[float, list[int]]:
        """Calcula o menor caminho entre dois vértices usando Dijkstra."""
        self._validar_vertice(origem)
        self._validar_vertice(destino)

        ignorados = set(ignorar_vertices or [])
        for v in ignorados:
            self._validar_vertice(v)

        if origem in ignorados or destino in ignorados:
            return math.inf, []

        distancias = [math.inf] * self.n
        anteriores: list[int | None] = [None] * self.n
        distancias[origem] = 0.0
        fila = [(0.0, origem)]

        while fila:
            distancia_atual, atual = heapq.heappop(fila)
            if distancia_atual != distancias[atual]:
                continue
            if atual == destino:
                break

            for vizinho in range(self.n):
                if vizinho in ignorados or not self._tem_aresta(atual, vizinho):
                    continue

                peso = float(self.adj[atual][vizinho]) if self.ponderado else 1.0
                if peso < 0:
                    raise ValueError(
                        "Dijkstra não pode ser aplicado a arestas com peso negativo."
                    )

                nova_distancia = distancia_atual + peso
                if nova_distancia < distancias[vizinho]:
                    distancias[vizinho] = nova_distancia
                    anteriores[vizinho] = atual
                    heapq.heappush(fila, (nova_distancia, vizinho))

        if math.isinf(distancias[destino]):
            return math.inf, []

        caminho = []
        atual: int | None = destino
        while atual is not None:
            caminho.append(atual)
            atual = anteriores[atual]
        caminho.reverse()

        return distancias[destino], caminho

    dijkstra = caminho_minimo

    # \1

    def _alcancaveis(self, origem: int) -> set[int]:
        self._validar_vertice(origem)

        visitados = {origem}
        fila = deque([origem])

        while fila:
            atual = fila.popleft()
            for vizinho in range(self.n):
                if self._tem_aresta(atual, vizinho) and vizinho not in visitados:
                    visitados.add(vizinho)
                    fila.append(vizinho)

        return visitados

    def categoria_conexidade(self) -> int:
        """Retorna 3=C3, 2=C2, 1=C1 ou 0=C0 para grafo orientado."""
        if self.n == 0:
            return 0

        alcancaveis = [self._alcancaveis(i) for i in range(self.n)]

        if all(len(alcancaveis[i]) == self.n for i in range(self.n)):
            return 3

        if all(
            j in alcancaveis[i] or i in alcancaveis[j]
            for i in range(self.n)
            for j in range(i + 1, self.n)
        ):
            return 2

        visitados = {0}
        fila = deque([0])

        while fila:
            atual = fila.popleft()
            for vizinho in range(self.n):
                adjacente = (
                    self._tem_aresta(atual, vizinho)
                    or self._tem_aresta(vizinho, atual)
                )
                if adjacente and vizinho not in visitados:
                    visitados.add(vizinho)
                    fila.append(vizinho)

        return 1 if len(visitados) == self.n else 0

    connectivityCategory = categoria_conexidade
    categoriaConexidade = categoria_conexidade

    def componentes_fortemente_conexas(self) -> list[set[int]]:
        if self.n == 0:
            return []

        alcancaveis = [self._alcancaveis(i) for i in range(self.n)]
        restantes = set(range(self.n))
        componentes = []

        while restantes:
            v = min(restantes)
            componente = {
                u for u in restantes
                if u in alcancaveis[v] and v in alcancaveis[u]
            }
            componentes.append(componente)
            restantes -= componente

        return componentes

    def grafo_reduzido(self) -> "Grafo":
        componentes = self.componentes_fortemente_conexas()
        reduzido = Grafo(len(componentes), tipo_grafo=4)

        if not componentes:
            return reduzido

        indice = {
            vertice: i
            for i, componente in enumerate(componentes)
            for vertice in componente
        }

        for v in range(self.n):
            for w in range(self.n):
                if self._tem_aresta(v, w) and indice[v] != indice[w]:
                    reduzido.insereA(indice[v], indice[w])

        return reduzido

    reducedGraph = grafo_reduzido
    grafoReduzido = grafo_reduzido

    # \1

    @classmethod
    def from_file(cls, nome_arquivo: str | Path) -> "Grafo":
        caminho = Path(nome_arquivo)
        linhas = [
            linha.strip()
            for linha in caminho.read_text(encoding="utf-8").splitlines()
            if linha.strip()
        ]

        if len(linhas) < 2:
            raise ValueError("Arquivo grafo.txt incompleto.")

        try:
            return cls._from_file(linhas)
        except (ValueError, IndexError):
            return cls._from_file_legado(linhas)

    @classmethod
    def _from_file(cls, linhas: list[str]) -> "Grafo":
        tipo = int(linhas[0])
        cls._validar_tipo(tipo)

        n = int(linhas[1])
        if n < 0:
            raise ValueError("Número de vértices inválido.")

        if len(linhas) < 2 + n + 1:
            raise ValueError("Formato do arquivo incompleto.")

        direcionado, peso_vertice, peso_aresta = TIPOS_GRAFO[tipo]
        classe_grafo = Grafo if direcionado else GrafoND
        grafo = classe_grafo(n, ponderado=peso_aresta, tipo_grafo=tipo)

        grafo.rotulos = ["" for _ in range(n)]
        grafo.pesos_vertices = [None for _ in range(n)]

        for linha in linhas[2:2 + n]:
            partes = shlex.split(linha)
            minimo = 3 if peso_vertice else 2
            if len(partes) < minimo:
                raise ValueError(f"Linha de vértice inválida: {linha}")

            indice = int(partes[0])
            grafo._validar_vertice(indice)
            grafo.rotulos[indice] = partes[1]

            if peso_vertice:
                grafo.pesos_vertices[indice] = float(partes[2])

        if any(not rotulo for rotulo in grafo.rotulos):
            raise ValueError("Todos os vértices devem possuir rótulo.")

        pos_m = 2 + n
        m_declarado = int(linhas[pos_m])
        arestas = linhas[pos_m + 1:]

        if len(arestas) != m_declarado:
            raise ValueError(
                f"Quantidade de arestas inconsistente: declarado {m_declarado}, "
                f"encontrado {len(arestas)}."
            )

        for linha in arestas:
            partes = shlex.split(linha)
            minimo = 3 if peso_aresta else 2
            if len(partes) < minimo:
                raise ValueError(f"Linha de aresta inválida: {linha}")

            v, w = int(partes[0]), int(partes[1])
            peso = float(partes[2]) if peso_aresta else None
            grafo.insereA(v, w, peso)

        if grafo.m != m_declarado:
            raise ValueError(
                "O número de arestas únicas carregadas não coincide com m. "
                "Em grafo não orientado, registre cada aresta apenas uma vez."
            )

        return grafo

    @classmethod
    def _from_file_legado(cls, linhas: list[str]) -> "Grafo":
        n = int(linhas[0])
        quantidade = int(linhas[1])
        dados = [shlex.split(linha) for linha in linhas[2:2 + quantidade]]

        if len(dados) != quantidade or any(len(partes) < 2 for partes in dados):
            raise ValueError("Formato legado inválido.")

        ponderado = any(len(partes) >= 3 for partes in dados)
        grafo = cls(n, ponderado=ponderado)

        for partes in dados:
            peso = float(partes[2]) if ponderado and len(partes) >= 3 else (1.0 if ponderado else None)
            grafo.insereA(int(partes[0]), int(partes[1]), peso)

        return grafo

    loadFromFile = from_file

    def salvar_arquivo(self, nome_arquivo: str | Path) -> None:
        """Grava o grafo no formato usado no projeto."""
        caminho = Path(nome_arquivo)
        linhas = [str(self.tipo_grafo), str(self.n)]

        for i in range(self.n):
            rotulo = self.rotulos[i].replace('"', "'")
            if self.peso_no_vertice:
                peso = self.pesos_vertices[i]
                if peso is None:
                    raise ValueError(f"Vértice {i} não possui peso.")
                linhas.append(f'{i} "{rotulo}" {peso}')
            else:
                linhas.append(f'{i} "{rotulo}"')

        linhas.append(str(self.m))

        for v, w, peso in self.iter_arestas():
            if self.peso_na_aresta:
                linhas.append(f"{v} {w} {peso}")
            else:
                linhas.append(f"{v} {w}")

        caminho.write_text("\n".join(linhas) + "\n", encoding="utf-8")

    saveToFile = salvar_arquivo

    def iter_arestas(self):
        for v in range(self.n):
            for w in range(self.n):
                if self._tem_aresta(v, w):
                    yield v, w, self.adj[v][w] if self.ponderado else None

    # \1

    def mostrar_lista_adjacencia(self) -> None:
        print(f"\nTipo: {self.tipo_grafo} | Vértices: {self.n} | Arestas: {self.m}")
        for v in range(self.n):
            vizinhos = []
            for w in range(self.n):
                if self._tem_aresta(v, w):
                    if self.ponderado:
                        vizinhos.append(f"{w}({self.adj[v][w]})")
                    else:
                        vizinhos.append(str(w))
            print(f"{v:3d} [{self.rotulos[v]}] -> " + ", ".join(vizinhos))

    def show(self) -> None:
        # Mantém o método usado nas atividades anteriores.
        print(f"\nn: {self.n:2d} m: {self.m:2d}")
        self.mostrar_lista_adjacencia()
        print("fim da impressao do grafo.")

    def showMin(self) -> None:
        self.show()


class GrafoPonderado(Grafo):
    """Compatibilidade com a atividade antiga de grafos dirigidos ponderados."""

    def __init__(self, n: int = Grafo.TAM_MAX_DEFAULT, ponderado: bool = True):
        super().__init__(n, ponderado=True, tipo_grafo=6)


class GrafoND(Grafo):
    """Grafo não dirigido representado por matriz de adjacência."""

    def __init__(
        self,
        n: int = Grafo.TAM_MAX_DEFAULT,
        ponderado: bool = False,
        *,
        tipo_grafo: int | None = None,
        rotulos: Iterable[str] | None = None,
        pesos_vertices: Iterable[float | None] | None = None,
    ) -> None:
        if tipo_grafo is None:
            tipo_grafo = 2 if ponderado else 0
        self._validar_tipo(tipo_grafo)

        direcionado, peso_vertice, peso_aresta = TIPOS_GRAFO[tipo_grafo]
        if direcionado:
            raise ValueError(
                "A classe GrafoND representa grafos não orientados. "
                "Use Grafo para tipos 4 a 7."
            )

        # Inicialização equivalente à classe base, sem acionar a restrição
        # de orientação presente em Grafo.__init__.
        if not isinstance(n, int) or n < 0:
            raise ValueError("A quantidade de vértices deve ser um inteiro não negativo.")

        self.tipo_grafo = tipo_grafo
        self.n = n
        self.m = 0
        self.ponderado = peso_aresta
        self.tem_peso_vertice = peso_vertice

        vazio = None if self.ponderado else 0
        self.adj = [[vazio for _ in range(n)] for _ in range(n)]
        self.rotulos = list(rotulos) if rotulos is not None else [str(i) for i in range(n)]
        self.pesos_vertices = (
            list(pesos_vertices)
            if pesos_vertices is not None
            else [None for _ in range(n)]
        )
        self._validar_metadados_vertices()

    def insereA(self, v: int, w: int, peso: float | None = None) -> None:
        self._validar_vertice(v)
        self._validar_vertice(w)

        if v == w:
            raise ValueError("Grafo não dirigido simples não aceita laços.")
        if self._tem_aresta(v, w):
            return

        if self.ponderado:
            if peso is None:
                raise ValueError("Este grafo exige peso na aresta.")
            valor = float(peso)
        else:
            valor = 1

        self.adj[v][w] = valor
        self.adj[w][v] = valor
        self.m += 1

    def removeA(self, v: int, w: int) -> None:
        self._validar_vertice(v)
        self._validar_vertice(w)

        if not self._tem_aresta(v, w):
            return

        vazio = None if self.ponderado else 0
        self.adj[v][w] = vazio
        self.adj[w][v] = vazio
        self.m -= 1

    def degree(self, v: int) -> int:
        self._validar_vertice(v)
        return sum(1 for w in range(self.n) if self._tem_aresta(v, w))

    def isSource(self, v: int) -> int:
        raise TypeError("Fonte é uma propriedade de grafos dirigidos.")

    def isSink(self, v: int) -> int:
        raise TypeError("Sorvedouro é uma propriedade de grafos dirigidos.")

    def isSymmetric(self) -> int:
        return 1

    def isComplete(self) -> int:
        return int(
            all(
                i == j or self._tem_aresta(i, j)
                for i in range(self.n)
                for j in range(self.n)
            )
        )

    def remove_vertex(self, v: int) -> None:
        self._validar_vertice(v)

        self.adj.pop(v)
        for linha in self.adj:
            linha.pop(v)

        self.rotulos.pop(v)
        self.pesos_vertices.pop(v)
        self.n -= 1

        self.m = sum(
            1
            for i in range(self.n)
            for j in range(i + 1, self.n)
            if self._tem_aresta(i, j)
        )

    removeV = remove_vertex
    removeVertice = remove_vertex

    def connectivity_type(self) -> int:
        """Retorna 0 se conexo e 1 se desconexo, conforme atividade da disciplina."""
        if self.n == 0:
            return 0
        return int(len(self._alcancaveis(0)) != self.n)

    connected = connectivity_type
    tipoConexidade = connectivity_type

    def eh_conexo(self) -> bool:
        return self.connectivity_type() == 0

    def componentes_conexas(
        self, ignorar_vertices: Iterable[int] | None = None
    ) -> list[set[int]]:
        """Retorna as componentes conexas, podendo ignorar vértices."""
        ignorados = set(ignorar_vertices or [])
        for v in ignorados:
            self._validar_vertice(v)

        restantes = set(range(self.n)) - ignorados
        componentes: list[set[int]] = []

        while restantes:
            origem = min(restantes)
            componente = {origem}
            fila = deque([origem])
            restantes.remove(origem)

            while fila:
                atual = fila.popleft()
                for vizinho in range(self.n):
                    if (
                        vizinho in restantes
                        and self._tem_aresta(atual, vizinho)
                    ):
                        restantes.remove(vizinho)
                        componente.add(vizinho)
                        fila.append(vizinho)

            componentes.append(componente)

        return componentes

    def vertices_da_mesma_estacao(self, v: int) -> list[int]:
        """Localiza todas as ocorrências estação-linha da mesma estação física."""
        self._validar_vertice(v)
        nome = self.rotulos[v].split("| Linha", 1)[0].strip()
        return [
            i
            for i, rotulo in enumerate(self.rotulos)
            if rotulo.split("| Linha", 1)[0].strip() == nome
        ]

    def simular_falha_estacao(self, v: int) -> dict:
        """Simula a indisponibilidade de uma estação sem modificar o grafo.

        Como o estudo de caso representa integrações por vértices estação-linha,
        a falha de uma estação física ignora todas as ocorrências dessa estação
        nas diferentes linhas.
        """
        self._validar_vertice(v)
        indisponiveis = self.vertices_da_mesma_estacao(v)
        antes = self.componentes_conexas()
        depois = self.componentes_conexas(indisponiveis)

        return {
            "nome": self.rotulos[v].split("| Linha", 1)[0].strip(),
            "vertices_indisponiveis": indisponiveis,
            "componentes_antes": antes,
            "componentes_depois": depois,
            "continua_conexo": len(depois) <= 1,
            "falha_critica": len(depois) > len(antes),
        }

    def complemento(self) -> "GrafoND":
        resultado = GrafoND(self.n, tipo_grafo=0)
        for i in range(self.n):
            for j in range(i + 1, self.n):
                if not self._tem_aresta(i, j):
                    resultado.insereA(i, j)
        return resultado

    def iter_arestas(self):
        """Em grafo não dirigido, cada aresta é devolvida uma única vez."""
        for v in range(self.n):
            for w in range(v + 1, self.n):
                if self._tem_aresta(v, w):
                    yield v, w, self.adj[v][w] if self.ponderado else None


TGrafo = Grafo
TGrafoND = GrafoND
