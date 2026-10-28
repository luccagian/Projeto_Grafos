# -*- coding: utf-8 -*-
"""
Integrantes:
Gabriel Medina - 10426931
Gian Lucca Campanha Ribeiro - 10438361
Lucas Carmo - 10439830

Arquivo: grafoLista.py
Resumo: implementação do grafo por lista de adjacência usada no projeto.
"""

from collections import deque
from pathlib import Path


class Grafo:
    TAM_MAX_DEFAULT = 100

    def __init__(self, n=TAM_MAX_DEFAULT):
        if n < 0:
            raise ValueError("A quantidade de vértices não pode ser negativa")
        self.n = n
        self.m = 0
        self.listaAdj = [[] for _ in range(n)]

    def _validar_vertice(self, v):
        if not isinstance(v, int) or not 0 <= v < self.n:
            raise IndexError(f"Vértice inválido: {v}")

    def insereA(self, v, w):
        self._validar_vertice(v)
        self._validar_vertice(w)
        if w not in self.listaAdj[v]:
            self.listaAdj[v].append(w)
            self.listaAdj[v].sort()
            self.m += 1

    def removeA(self, v, w):
        self._validar_vertice(v)
        self._validar_vertice(w)
        if w in self.listaAdj[v]:
            self.listaAdj[v].remove(w)
            self.m -= 1

    def inDegree(self, v):
        self._validar_vertice(v)
        return sum(v in vizinhos for vizinhos in self.listaAdj)

    def outDegree(self, v):
        self._validar_vertice(v)
        return len(self.listaAdj[v])

    def degree(self, v):
        return self.inDegree(v) + self.outDegree(v)

    def isSource(self, v):
        return int(self.outDegree(v) > 0 and self.inDegree(v) == 0)

    def isSink(self, v):
        return int(self.inDegree(v) > 0 and self.outDegree(v) == 0)

    fonte = isSource
    sorvedouro = isSink

    def isSymmetric(self):
        return int(all((j in self.listaAdj[i]) == (i in self.listaAdj[j])
                       for i in range(self.n) for j in range(self.n)))

    simetrico = isSymmetric

    def isComplete(self):
        return int(all(i == j or j in self.listaAdj[i]
                       for i in range(self.n) for j in range(self.n)))

    completo = isComplete

    def equals(self, outro):
        if not isinstance(outro, Grafo) or self.n != outro.n:
            return 0
        return int(all(set(self.listaAdj[i]) == set(outro.listaAdj[i])
                       for i in range(self.n)))

    igual = equals
    isEqual = equals

    def invert(self):
        for lista in self.listaAdj:
            lista.reverse()
        return self

    inverte = invert
    inverteListas = invert

    def remove_vertex(self, v):
        self._validar_vertice(v)
        self.listaAdj.pop(v)
        for vizinhos in self.listaAdj:
            vizinhos[:] = [w - 1 if w > v else w for w in vizinhos if w != v]
        self.n -= 1
        self.m = sum(len(vizinhos) for vizinhos in self.listaAdj)

    removeV = remove_vertex
    removeVertice = remove_vertex

    @classmethod
    def from_file(cls, nome_arquivo):
        linhas = [linha.split() for linha in Path(nome_arquivo).read_text(
            encoding="utf-8").splitlines() if linha.strip()]
        if len(linhas) < 2:
            raise ValueError("Arquivo deve conter V e A")
        n, quantidade = int(linhas[0][0]), int(linhas[1][0])
        dados = linhas[2:2 + quantidade]
        if len(dados) != quantidade or any(len(x) < 2 for x in dados):
            raise ValueError("Quantidade ou formato de arestas inválido")
        grafo = cls(n)
        for origem, destino, *_ in dados:
            grafo.insereA(int(origem), int(destino))
        return grafo

    loadFromFile = from_file

    @classmethod
    def from_matriz(cls, matriz):
        n = len(matriz.adj) if hasattr(matriz, "adj") else len(matriz)
        grafo = cls(n)
        valores = matriz.adj if hasattr(matriz, "adj") else matriz
        if any(len(linha) != n for linha in valores):
            raise ValueError("Matriz deve ser quadrada")
        for i in range(n):
            for j in range(n):
                valor = valores[i][j]
                presente = valor is not None and valor != 0
                if presente:
                    grafo.insereA(i, j)
        return grafo

    convertFromMatrix = from_matriz
    converteMatriz = from_matriz

    def to_matriz(self):
        try:
            from .grafoMatriz import Grafo as GrafoMatriz
        except ImportError:
            from grafoMatriz import Grafo as GrafoMatriz
        matriz = GrafoMatriz(self.n)
        for i, vizinhos in enumerate(self.listaAdj):
            for j in vizinhos:
                matriz.insereA(i, j)
        return matriz

    toMatrix = to_matriz
    converte = to_matriz

    def _alcancaveis(self, origem):
        visitados = {origem}
        fila = deque([origem])
        while fila:
            atual = fila.popleft()
            for vizinho in self.listaAdj[atual]:
                if vizinho not in visitados:
                    visitados.add(vizinho)
                    fila.append(vizinho)
        return visitados

    def show(self):
        print(f"\nn: {self.n:2d} m: {self.m:2d}")
        for i, vizinhos in enumerate(self.listaAdj):
            print(f"{i:2d}: " + " ".join(str(v) for v in vizinhos))
        print("fim da impressao do grafo.")


class GrafoND(Grafo):
    def insereA(self, v, w):
        self._validar_vertice(v)
        self._validar_vertice(w)
        if v == w:
            raise ValueError("Grafo não dirigido simples não aceita laços")
        if w in self.listaAdj[v]:
            return
        self.listaAdj[v].append(w)
        self.listaAdj[w].append(v)
        self.listaAdj[v].sort()
        self.listaAdj[w].sort()
        self.m += 1

    def removeA(self, v, w):
        self._validar_vertice(v)
        self._validar_vertice(w)
        if w in self.listaAdj[v]:
            self.listaAdj[v].remove(w)
            self.listaAdj[w].remove(v)
            self.m -= 1

    def degree(self, v):
        self._validar_vertice(v)
        return len(self.listaAdj[v])

    def isSource(self, v):
        raise TypeError("Fonte é uma propriedade de grafos dirigidos")

    def isSink(self, v):
        raise TypeError("Sorvedouro é uma propriedade de grafos dirigidos")

    def isSymmetric(self):
        return 1

    def connectivity_type(self):
        if self.n == 0:
            return 0
        return int(len(self._alcancaveis(0)) != self.n)

    connected = connectivity_type
    tipoConexidade = connectivity_type

    def remove_vertex(self, v):
        self._validar_vertice(v)
        self.listaAdj.pop(v)
        for vizinhos in self.listaAdj:
            vizinhos[:] = [w - 1 if w > v else w for w in vizinhos if w != v]
        self.n -= 1
        self.m = sum(len(vizinhos) for vizinhos in self.listaAdj) // 2

    removeV = remove_vertex
    removeVertice = remove_vertex

    def complemento(self):
        resultado = self.__class__(self.n)
        for i in range(self.n):
            for j in range(i + 1, self.n):
                if j not in self.listaAdj[i]:
                    resultado.insereA(i, j)
        return resultado


TGrafo = Grafo
TGrafoND = GrafoND
