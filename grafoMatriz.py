# -*- coding: utf-8 -*-
from collections import deque
from pathlib import Path


class Grafo:
    TAM_MAX_DEFAULT = 100

    def __init__(self, n=TAM_MAX_DEFAULT, ponderado=False):
        if n < 0:
            raise ValueError("A quantidade de vértices não pode ser negativa")
        self.n = n
        self.m = 0
        self.ponderado = ponderado
        vazio = None if ponderado else 0
        self.adj = [[vazio for _ in range(n)] for _ in range(n)]

    def _validar_vertice(self, v):
        if not isinstance(v, int) or not 0 <= v < self.n:
            raise IndexError(f"Vértice inválido: {v}")

    def _tem_aresta(self, v, w):
        return self.adj[v][w] is not None if self.ponderado else self.adj[v][w] != 0

    def insereA(self, v, w, peso=None):
        self._validar_vertice(v)
        self._validar_vertice(w)
        if self._tem_aresta(v, w):
            return
        self.adj[v][w] = (1.0 if peso is None else float(peso)) if self.ponderado else 1
        self.m += 1

    def removeA(self, v, w):
        self._validar_vertice(v)
        self._validar_vertice(w)
        if self._tem_aresta(v, w):
            self.adj[v][w] = None if self.ponderado else 0
            self.m -= 1

    def inDegree(self, v):
        self._validar_vertice(v)
        return sum(1 for u in range(self.n) if self._tem_aresta(u, v))

    def outDegree(self, v):
        self._validar_vertice(v)
        return sum(1 for w in range(self.n) if self._tem_aresta(v, w))

    def degree(self, v):
        return self.inDegree(v) + self.outDegree(v)

    def isSource(self, v):
        return int(self.outDegree(v) > 0 and self.inDegree(v) == 0)

    def isSink(self, v):
        return int(self.inDegree(v) > 0 and self.outDegree(v) == 0)

    fonte = isSource
    sorvedouro = isSink

    def isSymmetric(self):
        return int(all(self._tem_aresta(i, j) == self._tem_aresta(j, i)
                       for i in range(self.n) for j in range(self.n)))

    simetrico = isSymmetric

    def isComplete(self):
        return int(all(i == j or self._tem_aresta(i, j)
                       for i in range(self.n) for j in range(self.n)))

    completo = isComplete

    def remove_vertex(self, v):
        self._validar_vertice(v)
        self.adj.pop(v)
        for linha in self.adj:
            linha.pop(v)
        self.n -= 1
        self.m = sum(1 for i in range(self.n) for j in range(self.n)
                     if self._tem_aresta(i, j))

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
        ponderado = any(len(x) >= 3 for x in dados)
        grafo = cls(n, ponderado=ponderado)
        for partes in dados:
            grafo.insereA(int(partes[0]), int(partes[1]),
                          float(partes[2]) if ponderado and len(partes) >= 3 else None)
        return grafo

    loadFromFile = from_file

    def _alcancaveis(self, origem):
        visitados = {origem}
        fila = deque([origem])
        while fila:
            atual = fila.popleft()
            for vizinho in range(self.n):
                if self._tem_aresta(atual, vizinho) and vizinho not in visitados:
                    visitados.add(vizinho)
                    fila.append(vizinho)
        return visitados

    def complemento(self):
        resultado = self.__class__(self.n, ponderado=False)
        for i in range(self.n):
            for j in range(self.n):
                if i != j and not self._tem_aresta(i, j):
                    resultado.insereA(i, j)
        return resultado

    complement = complemento

    def categoria_conexidade(self):
        if self.n == 0:
            return 0
        alc = [self._alcancaveis(i) for i in range(self.n)]
        if all(len(alc[i]) == self.n for i in range(self.n)):
            return 3  # fortemente conexo
        if all(j in alc[i] or i in alc[j]
               for i in range(self.n) for j in range(i + 1, self.n)):
            return 2  # unilateralmente conexo
        visitados = {0}
        fila = deque([0])
        while fila:
            atual = fila.popleft()
            for vizinho in range(self.n):
                if (self._tem_aresta(atual, vizinho) or
                        self._tem_aresta(vizinho, atual)) and vizinho not in visitados:
                    visitados.add(vizinho)
                    fila.append(vizinho)
        return 1 if len(visitados) == self.n else 0  # fracamente conexo/desconexo

    connectivityCategory = categoria_conexidade
    categoriaConexidade = categoria_conexidade

    def grafo_reduzido(self):
        if self.n == 0:
            return Grafo(0)
        alc = [self._alcancaveis(i) for i in range(self.n)]
        componentes = []
        restantes = set(range(self.n))
        while restantes:
            v = min(restantes)
            comp = {u for u in restantes if u in alc[v] and v in alc[u]}
            componentes.append(comp)
            restantes -= comp
        indice = {v: c for c, comp in enumerate(componentes) for v in comp}
        reduzido = Grafo(len(componentes))
        for v in range(self.n):
            for w in range(self.n):
                if self._tem_aresta(v, w) and indice[v] != indice[w]:
                    reduzido.insereA(indice[v], indice[w])
        return reduzido

    reducedGraph = grafo_reduzido
    grafoReduzido = grafo_reduzido

    def show(self):
        print(f"\nn: {self.n:2d} m: {self.m:2d}")
        for linha in self.adj:
            print(" ".join(str(valor) for valor in linha))
        print("fim da impressao do grafo.")

    def showMin(self):
        self.show()


class GrafoPonderado(Grafo):
    def __init__(self, n=Grafo.TAM_MAX_DEFAULT, ponderado=True):
        super().__init__(n, ponderado=True)


class GrafoND(Grafo):
    def insereA(self, v, w, peso=None):
        self._validar_vertice(v)
        self._validar_vertice(w)
        if v == w:
            raise ValueError("Grafo não dirigido simples não aceita laços")
        if self._tem_aresta(v, w):
            return
        valor = (1.0 if peso is None else float(peso)) if self.ponderado else 1
        self.adj[v][w] = valor
        self.adj[w][v] = valor
        self.m += 1

    def removeA(self, v, w):
        self._validar_vertice(v)
        self._validar_vertice(w)
        if self._tem_aresta(v, w):
            vazio = None if self.ponderado else 0
            self.adj[v][w] = vazio
            self.adj[w][v] = vazio
            self.m -= 1

    def degree(self, v):
        self._validar_vertice(v)
        return sum(1 for w in range(self.n) if self._tem_aresta(v, w))

    def isSource(self, v):
        raise TypeError("Fonte é uma propriedade de grafos dirigidos")

    def isSink(self, v):
        raise TypeError("Sorvedouro é uma propriedade de grafos dirigidos")

    def isSymmetric(self):
        return 1

    def isComplete(self):
        return int(all(i == j or self._tem_aresta(i, j)
                       for i in range(self.n) for j in range(self.n)))

    def remove_vertex(self, v):
        self._validar_vertice(v)
        self.adj.pop(v)
        for linha in self.adj:
            linha.pop(v)
        self.n -= 1
        # Cada aresta não dirigida ocupa duas posições simétricas.
        self.m = sum(1 for i in range(self.n) for j in range(i + 1, self.n)
                     if self._tem_aresta(i, j))

    removeV = remove_vertex
    removeVertice = remove_vertex

    def connectivity_type(self):
        if self.n == 0:
            return 0
        return int(len(self._alcancaveis(0)) != self.n)

    connected = connectivity_type
    tipoConexidade = connectivity_type

    def complemento(self):
        resultado = self.__class__(self.n, ponderado=False)
        for i in range(self.n):
            for j in range(i + 1, self.n):
                if not self._tem_aresta(i, j):
                    resultado.insereA(i, j)
        return resultado


TGrafo = Grafo
TGrafoND = GrafoND
