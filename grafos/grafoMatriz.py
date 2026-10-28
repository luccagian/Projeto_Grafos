"""
Integrantes:
Gabriel Medina - 10426931
Gian Lucca Campanha Ribeiro - 10438361
Lucas Carmo - 10439830

Arquivo: grafoMatriz.py
Resumo: implementação do grafo por matriz de adjacência usada no projeto.
"""

from collections import deque
from pathlib import Path
import heapq
import math
import shlex


class Grafo:
    TAM_MAX_DEFAULT = 100

    def __init__(
        self,
        n=TAM_MAX_DEFAULT,
        ponderado=None,
        tipo_grafo=None,
        rotulos=None,
        pesos_vertices=None
    ):
        if n < 0:
            raise ValueError('A quantidade de vértices não pode ser negativa')

        self.n = n
        self.m = 0
        if tipo_grafo is None:
            if isinstance(self, GrafoND):
                tipo_grafo = 2 if ponderado else 0
            else:
                tipo_grafo = 6 if ponderado else 4
        if tipo_grafo not in range(8):
            raise ValueError("O tipo do grafo deve estar entre 0 e 7.")
        if isinstance(self, GrafoND) != (tipo_grafo < 4):
            raise ValueError("O tipo informado não corresponde à classe do grafo.")

        tem_peso_aresta = tipo_grafo in (2, 3, 6, 7)
        if ponderado is not None and ponderado != tem_peso_aresta:
            raise ValueError("O parâmetro ponderado não corresponde ao tipo do grafo.")
        self.tipo_grafo = tipo_grafo
        self.ponderado = tem_peso_aresta
        self.pesos_vertices = list(pesos_vertices) if pesos_vertices is not None else [None] * n
        if len(self.pesos_vertices) != n:
            raise ValueError("Quantidade de pesos de vértices inválida.")

        if rotulos is None:
            self.rotulos = [f"Vértice {i}" for i in range(n)]
        elif isinstance(rotulos, dict):
            self.rotulos = [rotulos[i] for i in range(n)]
        else:
            self.rotulos = list(rotulos)
        if len(self.rotulos) != n:
            raise ValueError("Quantidade de rótulos inválida.")

        vazio = None if self.ponderado else 0

        self.adj = [[vazio for _ in range(n)] for _ in range(n)]

    # Validação

    def _validar_vertice(self, v):
        if not isinstance(v, int) or not 0 <= v < self.n:
            raise IndexError(f'Vértice inválido: {v}')

    def _tem_aresta(self, v, w):
        if self.ponderado:
            return self.adj[v][w] is not None

        return self.adj[v][w] != 0

    # Vértices

    def nome_vertice(self, v):
        self._validar_vertice(v)

        return self.rotulos[v]

    def inserir_vertice(self, nome=None, peso=None):
        novo_id = self.n
        vazio = None if self.ponderado else 0
        for linha in self.adj:
            linha.append(vazio)
        self.adj.append([vazio] * (self.n + 1))
        self.n += 1
        self.rotulos.append(nome.strip() if nome and nome.strip() else f"Vértice {novo_id}")
        self.pesos_vertices.append(peso)
        return novo_id

    # Arestas

    def insereA(self, v, w, peso=None):
        self._validar_vertice(v)
        self._validar_vertice(w)

        if self._tem_aresta(v, w):
            return

        if self.ponderado:
            valor = 1.0 if peso is None else float(peso)
        else:
            valor = 1

        self.adj[v][w] = valor

        self.m += 1

    def removeA(self, v, w):
        self._validar_vertice(v)
        self._validar_vertice(w)

        if not self._tem_aresta(v, w):
            return

        self.adj[v][w] = None if self.ponderado else 0

        self.m -= 1

    # Graus

    def inDegree(self, v):
        self._validar_vertice(v)

        return sum(1 for u in range(self.n) if self._tem_aresta(u, v))

    def outDegree(self, v):
        self._validar_vertice(v)

        return sum(1 for w in range(self.n) if self._tem_aresta(v, w))

    def degree(self, v):
        return self.inDegree(v) + self.outDegree(v)

    # Remoção de vértice

    def remove_vertex(self, v):
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

    # Alcance

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

    # Conexidade para grafo dirigido

    def categoria_conexidade(self):
        if self.n == 0:
            return 0

        alc = [self._alcancaveis(i) for i in range(self.n)]

        if all(len(alc[i]) == self.n for i in range(self.n)):
            return 3

        if all(
            j in alc[i]
            or i in alc[j]
            for i in range(self.n)
            for j in range(i + 1, self.n)
        ):
            return 2

        visitados = {0}

        fila = deque([0])

        while fila:
            atual = fila.popleft()

            for vizinho in range(self.n):
                conectado = self._tem_aresta(atual, vizinho) or self._tem_aresta(vizinho, atual)
                if conectado and vizinho not in visitados:
                    visitados.add(vizinho)

                    fila.append(vizinho)

        if len(visitados) == self.n:
            return 1

        return 0

    # Grafo reduzido

    def grafo_reduzido(self):
        if self.n == 0:
            return Grafo(0)

        alc = [self._alcancaveis(i) for i in range(self.n)]

        componentes = []

        restantes = set(range(self.n))

        while restantes:
            v = min(restantes)

            componente = {u for u in restantes if u in alc[v] and v in alc[u]}

            componentes.append(componente)

            restantes -= componente

        indice = {v: i for i, comp in enumerate(componentes) for v in comp}

        reduzido = Grafo(len(componentes))

        for v in range(self.n):
            for w in range(self.n):
                if self._tem_aresta(v, w) and indice[v] != indice[w]:
                    reduzido.insereA(indice[v], indice[w])

        return reduzido

    # Mostrar

    def show(self):
        print(
            f"\nn: {self.n} | Tipo: {self.tipo_grafo}"
            f" | Vértices: {self.n}"
            f" | Arestas: {self.m}"
        )

        for i in range(self.n):
            vizinhos = []

            for j in range(self.n):
                if self._tem_aresta(i, j):
                    peso = self.adj[i][j]

                    vizinhos.append(f'{j}({peso})')

            nome = self.nome_vertice(i)

            print(f'{i:3d} [{nome}] -> ' + ', '.join(vizinhos))

        print("fim da impressao")

    # Propriedades e verificações

    @property
    def direcionado(self):
        return not isinstance(self, GrafoND)

    @property
    def peso_no_vertice(self):
        return self.tipo_grafo in (1, 3, 5, 7)

    @property
    def peso_na_aresta(self):
        return self.ponderado

    def isSource(self, v):
        return int(self.inDegree(v) == 0 and self.outDegree(v) > 0)

    def isSink(self, v):
        return int(self.outDegree(v) == 0 and self.inDegree(v) > 0)

    def isSymmetric(self):
        return int(all(self._tem_aresta(i, j) == self._tem_aresta(j, i)
                       for i in range(self.n) for j in range(self.n)))

    def isComplete(self):
        return int(all(self._tem_aresta(i, j) for i in range(self.n)
                       for j in range(self.n) if i != j))

    def complemento(self):
        resultado = GrafoND(self.n) if isinstance(self, GrafoND) else Grafo(self.n)
        for i in range(self.n):
            for j in range(self.n):
                if i != j and not self._tem_aresta(i, j):
                    resultado.insereA(i, j)
        return resultado

    def caminho_minimo(self, origem, destino):
        self._validar_vertice(origem)
        self._validar_vertice(destino)
        for i in range(self.n):
            for j in range(self.n):
                if self._tem_aresta(i, j) and (not math.isfinite(self.adj[i][j]) or self.adj[i][j] < 0):
                    raise ValueError("Dijkstra exige pesos finitos e não negativos.")
        distancias = [math.inf] * self.n
        anterior = [None] * self.n
        distancias[origem] = 0
        fila = [(0, origem)]
        while fila:
            distancia, atual = heapq.heappop(fila)
            if distancia != distancias[atual]:
                continue
            if atual == destino:
                break
            for vizinho in range(self.n):
                if self._tem_aresta(atual, vizinho):
                    nova = distancia + self.adj[atual][vizinho]
                    if nova < distancias[vizinho]:
                        distancias[vizinho] = nova
                        anterior[vizinho] = atual
                        heapq.heappush(fila, (nova, vizinho))
        if math.isinf(distancias[destino]):
            return math.inf, []
        caminho = []
        atual = destino
        while atual is not None:
            caminho.append(atual)
            atual = anterior[atual]
        return distancias[destino], caminho[::-1]

    # Leitura e gravação

    @classmethod
    def from_file(cls, nome_arquivo):
        linhas = [linha.strip() for linha in Path(nome_arquivo).read_text(encoding="utf-8").splitlines() if linha.strip()]
        if len(linhas) < 2:
            raise ValueError("Arquivo de grafo incompleto.")
        # Formato antigo dos exercícios: n, m e pares de vértices.
        primeiro, segundo = int(linhas[0]), int(linhas[1])
        if len(linhas) == segundo + 2 and all(len(linha.split()) == 2 for linha in linhas[2:]):
            grafo = cls(primeiro)
            for linha in linhas[2:]:
                v, w = map(int, linha.split())
                grafo.insereA(v, w)
            return grafo
        tipo, n = primeiro, segundo
        if tipo not in range(8) or n < 0 or len(linhas) < n + 3:
            raise ValueError("Cabeçalho de grafo inválido.")
        rotulos, pesos = [], []
        peso_vertice = tipo in (1, 3, 5, 7)
        peso_aresta = tipo in (2, 3, 6, 7)
        for i, linha in enumerate(linhas[2:2+n]):
            partes = shlex.split(linha)
            if len(partes) < (3 if peso_vertice else 2) or int(partes[0]) != i:
                raise ValueError("Vértice inválido ou fora de ordem.")
            rotulos.append(" ".join(partes[1:-1] if peso_vertice else partes[1:]))
            pesos.append(float(partes[-1]) if peso_vertice else None)
        m = int(linhas[2+n])
        if m < 0 or len(linhas) != n + 3 + m:
            raise ValueError("Quantidade de arestas inválida.")
        classe = GrafoND if tipo < 4 else Grafo
        grafo = classe(n, ponderado=peso_aresta, tipo_grafo=tipo, rotulos=rotulos, pesos_vertices=pesos)
        for linha in linhas[3+n:]:
            partes = linha.split()
            if len(partes) != (3 if peso_aresta else 2):
                raise ValueError("Aresta inválida.")
            v, w = map(int, partes[:2])
            grafo._validar_vertice(v)
            grafo._validar_vertice(w)
            if grafo._tem_aresta(v, w):
                raise ValueError("Aresta duplicada.")
            grafo.insereA(v, w, float(partes[2]) if peso_aresta else None)
        return grafo

    def to_file(self, nome_arquivo):
        arestas = [(i, j) for i in range(self.n) for j in range(self.n)
                   if (self.direcionado or i < j) and self._tem_aresta(i, j)]
        if self.peso_no_vertice and any(peso is None for peso in self.pesos_vertices):
            raise ValueError("Informe o peso de todos os vértices antes de salvar.")
        with Path(nome_arquivo).open("w", encoding="utf-8") as arquivo:
            arquivo.write(f"{self.tipo_grafo}\n{self.n}\n")
            for i, nome in enumerate(self.rotulos):
                peso = f" {self.pesos_vertices[i]}" if self.peso_no_vertice else ""
                arquivo.write(f"{i} {shlex.quote(nome)}{peso}\n")
            arquivo.write(f"{len(arestas)}\n")
            for i, j in arestas:
                peso = f" {self.adj[i][j]}" if self.ponderado else ""
                arquivo.write(f"{i} {j}{peso}\n")


class GrafoPonderado(Grafo):
    def __init__(self, n=Grafo.TAM_MAX_DEFAULT, rotulos=None):
        super().__init__(n, tipo_grafo=6, rotulos=rotulos)


class GrafoND(Grafo):
    def insereA(self, v, w, peso=None):
        self._validar_vertice(v)
        self._validar_vertice(w)

        if v == w:
            raise ValueError('Grafo não orientado simples não aceita laços.')

        if self._tem_aresta(v, w):
            return

        if self.ponderado:
            valor = 1.0 if peso is None else float(peso)

        else:
            valor = 1

        self.adj[v][w] = valor
        self.adj[w][v] = valor

        self.m += 1

    def removeA(self, v, w):
        self._validar_vertice(v)
        self._validar_vertice(w)

        if not self._tem_aresta(v, w):
            return

        vazio = None if self.ponderado else 0

        self.adj[v][w] = vazio
        self.adj[w][v] = vazio

        self.m -= 1

    def degree(self, v):
        self._validar_vertice(v)

        return sum(1 for w in range(self.n) if self._tem_aresta(v, w))

    def connectivity_type(self):
        if self.n == 0:
            return 0

        visitados = self._alcancaveis(0)

        return int(len(visitados) != self.n)

    def is_connected(self):
        if self.n == 0:
            return True

        return len(self._alcancaveis(0)) == self.n

    def componentes_conexas(self, excluidos=()):
        restantes = set(range(self.n)) - set(excluidos)
        componentes = []
        while restantes:
            inicio = next(iter(restantes))
            componente = {inicio}
            fila = deque([inicio])
            restantes.remove(inicio)
            while fila:
                atual = fila.popleft()
                vizinhos = [v for v in restantes if self._tem_aresta(atual, v)]
                for v in vizinhos:
                    restantes.remove(v)
                    componente.add(v)
                    fila.append(v)
            componentes.append(sorted(componente))
        return componentes

    def simular_falha_estacao(self, vertice):
        self._validar_vertice(vertice)
        nome = self.rotulos[vertice].split("|", 1)[0].strip()
        indisponiveis = [i for i, rotulo in enumerate(self.rotulos)
                         if rotulo.split("|", 1)[0].strip().casefold() == nome.casefold()]
        antes = self.componentes_conexas()
        depois = self.componentes_conexas(indisponiveis)
        return {"nome": nome, "vertices_indisponiveis": indisponiveis,
                "componentes_antes": antes, "componentes_depois": depois,
                "continua_conexo": len(depois) <= 1,
                "falha_critica": len(depois) > len(antes)}

    def remove_vertex(self, v):
        super().remove_vertex(v)
        # A matriz não orientada registra cada aresta nos dois sentidos.
        self.m //= 2
