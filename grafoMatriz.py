# -*- coding: utf-8 -*-
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


class Grafo:
    TAM_MAX_DEFAULT = 100

    def __init__(
        self,
        n=TAM_MAX_DEFAULT,
        ponderado=False,
        tipo=0,
        rotulos=None
    ):
        if n < 0:
            raise ValueError(
                "A quantidade de vértices não pode ser negativa"
            )

        self.n = n
        self.m = 0
        self.tipo = tipo
        self.ponderado = ponderado

        if rotulos is None:
            self.rotulos = {
                i: f"Vértice {i}"
                for i in range(n)
            }
        else:
            self.rotulos = dict(rotulos)

        vazio = None if ponderado else 0

        self.adj = [
            [vazio for _ in range(n)]
            for _ in range(n)
        ]

    # Validação

    def _validar_vertice(self, v):
        if not isinstance(v, int) or not 0 <= v < self.n:
            raise IndexError(
                f"Vértice inválido: {v}"
            )

    def _tem_aresta(self, v, w):
        if self.ponderado:
            return self.adj[v][w] is not None

        return self.adj[v][w] != 0

    # Vértices

    def nome_vertice(self, v):
        self._validar_vertice(v)

        return self.rotulos.get(
            v,
            f"Vértice {v}"
        )

    def inserir_vertice(self, nome=None):
        novo_id = self.n

        vazio = None if self.ponderado else 0

        for linha in self.adj:
            linha.append(vazio)

        self.adj.append(
            [vazio] * (self.n + 1)
        )

        self.n += 1

        if nome is None or not nome.strip():
            nome = f"Vértice {novo_id}"

        self.rotulos[novo_id] = nome

        return novo_id

    insereV = inserir_vertice

    # Arestas

    def insereA(self, v, w, peso=None):
        self._validar_vertice(v)
        self._validar_vertice(w)

        if self._tem_aresta(v, w):
            return

        if self.ponderado:
            valor = (
                1.0
                if peso is None
                else float(peso)
            )
        else:
            valor = 1

        self.adj[v][w] = valor

        self.m += 1

    def removeA(self, v, w):
        self._validar_vertice(v)
        self._validar_vertice(w)

        if not self._tem_aresta(v, w):
            return

        self.adj[v][w] = (
            None
            if self.ponderado
            else 0
        )

        self.m -= 1

    # Graus

    def inDegree(self, v):
        self._validar_vertice(v)

        return sum(
            1
            for u in range(self.n)
            if self._tem_aresta(u, v)
        )

    def outDegree(self, v):
        self._validar_vertice(v)

        return sum(
            1
            for w in range(self.n)
            if self._tem_aresta(v, w)
        )

    def degree(self, v):
        return (
            self.inDegree(v)
            + self.outDegree(v)
        )

    # Remoção de vértice

    def remove_vertex(self, v):
        self._validar_vertice(v)

        self.adj.pop(v)

        for linha in self.adj:
            linha.pop(v)

        novos_rotulos = {}

        for antigo_id, nome in self.rotulos.items():

            if antigo_id == v:
                continue

            novo_id = (
                antigo_id - 1
                if antigo_id > v
                else antigo_id
            )

            novos_rotulos[novo_id] = nome

        self.rotulos = novos_rotulos

        self.n -= 1

        self.m = sum(
            1
            for i in range(self.n)
            for j in range(self.n)
            if self._tem_aresta(i, j)
        )

    removeV = remove_vertex
    removeVertice = remove_vertex

    # Alcance

    def _alcancaveis(self, origem):

        visitados = {origem}

        fila = deque([origem])

        while fila:

            atual = fila.popleft()

            for vizinho in range(self.n):

                if (
                    self._tem_aresta(
                        atual,
                        vizinho
                    )
                    and vizinho
                    not in visitados
                ):

                    visitados.add(
                        vizinho
                    )

                    fila.append(
                        vizinho
                    )

        return visitados

    # Conexidade para grafo dirigido

    def categoria_conexidade(self):

        if self.n == 0:
            return 0

        alc = [
            self._alcancaveis(i)
            for i in range(self.n)
        ]

        if all(
            len(alc[i]) == self.n
            for i in range(self.n)
        ):
            return 3

        if all(
            j in alc[i]
            or i in alc[j]
            for i in range(self.n)
            for j in range(
                i + 1,
                self.n
            )
        ):
            return 2

        visitados = {0}

        fila = deque([0])

        while fila:

            atual = fila.popleft()

            for vizinho in range(
                self.n
            ):

                if (
                    (
                        self._tem_aresta(
                            atual,
                            vizinho
                        )
                        or
                        self._tem_aresta(
                            vizinho,
                            atual
                        )
                    )
                    and
                    vizinho
                    not in visitados
                ):

                    visitados.add(
                        vizinho
                    )

                    fila.append(
                        vizinho
                    )

        if len(visitados) == self.n:
            return 1

        return 0

    # Grafo reduzido

    def grafo_reduzido(self):

        if self.n == 0:
            return Grafo(0)

        alc = [
            self._alcancaveis(i)
            for i in range(self.n)
        ]

        componentes = []

        restantes = set(
            range(self.n)
        )

        while restantes:

            v = min(restantes)

            componente = {
                u
                for u in restantes
                if (
                    u in alc[v]
                    and v in alc[u]
                )
            }

            componentes.append(
                componente
            )

            restantes -= componente

        indice = {
            v: i
            for i, comp
            in enumerate(componentes)
            for v in comp
        }

        reduzido = Grafo(
            len(componentes)
        )

        for v in range(self.n):

            for w in range(self.n):

                if (
                    self._tem_aresta(v, w)
                    and
                    indice[v]
                    != indice[w]
                ):

                    reduzido.insereA(
                        indice[v],
                        indice[w]
                    )

        return reduzido

    # Mostrar

    def show(self):

        print(
            f"\nTipo: {self.tipo}"
            f" | Vértices: {self.n}"
            f" | Arestas: {self.m}"
        )

        for i in range(self.n):

            vizinhos = []

            for j in range(self.n):

                if self._tem_aresta(i, j):

                    peso = self.adj[i][j]

                    vizinhos.append(
                        f"{j}({peso})"
                    )

            nome = self.nome_vertice(i)

            print(
                f"{i:3d} "
                f"[{nome}] -> "
                + ", ".join(vizinhos)
            )

    # Leitura do grafo.txt

    @classmethod
    def from_file(
        cls,
        nome_arquivo
    ):

        caminho = Path(
            nome_arquivo
        )

        linhas = [
            linha.strip()
            for linha
            in caminho.read_text(
                encoding="utf-8"
            ).splitlines()
            if linha.strip()
        ]

        if len(linhas) < 3:
            raise ValueError(
                "Arquivo grafo.txt inválido."
            )

        indice = 0

        # Tipo do grafo
        tipo = int(
            linhas[indice]
        )

        indice += 1

        # Número de vértices
        n = int(
            linhas[indice]
        )

        indice += 1

        ponderado = tipo in (
            1, 2, 3,
            5, 6, 7
        )

        rotulos = {}

        # Vértices
        for _ in range(n):

            partes = linhas[indice].split(
                maxsplit=1
            )

            indice += 1

            vertice = int(
                partes[0]
            )

            if len(partes) > 1:
                nome = partes[1]
            else:
                nome = (
                    f"Vértice {vertice}"
                )

            rotulos[
                vertice
            ] = nome

        # Número de arestas
        m_arquivo = int(
            linhas[indice]
        )

        indice += 1

        # Determina se é não orientado
        nao_orientado = (
            tipo <= 3
        )

        classe = (
            GrafoND
            if nao_orientado
            else cls
        )

        grafo = classe(
            n=n,
            ponderado=ponderado,
            tipo=tipo,
            rotulos=rotulos
        )

        # Arestas
        for _ in range(m_arquivo):

            if indice >= len(linhas):
                raise ValueError(
                    "Quantidade de arestas "
                    "menor que o valor informado."
                )

            partes = (
                linhas[indice].split()
            )

            indice += 1

            if len(partes) < 2:
                raise ValueError(
                    "Aresta inválida."
                )

            origem = int(
                partes[0]
            )

            destino = int(
                partes[1]
            )

            peso = None

            if len(partes) >= 3:
                peso = float(
                    partes[2]
                )

            grafo.insereA(
                origem,
                destino,
                peso
            )

        return grafo

    loadFromFile = from_file

    # Gravação

    def to_file(
        self,
        nome_arquivo
    ):

        with open(
            nome_arquivo,
            "w",
            encoding="utf-8"
        ) as arquivo:

            # Tipo
            arquivo.write(
                f"{self.tipo}\n"
            )

            # Número de vértices
            arquivo.write(
                f"{self.n}\n"
            )

            # Vértices
            for i in range(
                self.n
            ):

                nome = (
                    self.nome_vertice(i)
                )

                arquivo.write(
                    f"{i} {nome}\n"
                )

            # Arestas
            arestas = []

            nao_orientado = (
                self.tipo <= 3
            )

            for i in range(
                self.n
            ):

                inicio = (
                    i + 1
                    if nao_orientado
                    else 0
                )

                for j in range(
                    inicio,
                    self.n
                ):

                    if not self._tem_aresta(
                        i,
                        j
                    ):
                        continue

                    peso = (
                        self.adj[i][j]
                    )

                    arestas.append(
                        (
                            i,
                            j,
                            peso
                        )
                    )

            arquivo.write(
                f"{len(arestas)}\n"
            )

            for (
                origem,
                destino,
                peso
            ) in arestas:

                if self.ponderado:

                    arquivo.write(
                        f"{origem} "
                        f"{destino} "
                        f"{peso}\n"
                    )

                else:

                    arquivo.write(
                        f"{origem} "
                        f"{destino}\n"
                    )


class GrafoPonderado(Grafo):

    def __init__(
        self,
        n=Grafo.TAM_MAX_DEFAULT,
        ponderado=True,
        tipo=6,
        rotulos=None
    ):

        super().__init__(
            n=n,
            ponderado=True,
            tipo=tipo,
            rotulos=rotulos
        )


class GrafoND(Grafo):

    def insereA(
        self,
        v,
        w,
        peso=None
    ):

        self._validar_vertice(v)
        self._validar_vertice(w)

        if v == w:
            raise ValueError(
                "Grafo não orientado "
                "simples não aceita laços."
            )

        if self._tem_aresta(v, w):
            return

        if self.ponderado:

            valor = (
                1.0
                if peso is None
                else float(peso)
            )

        else:
            valor = 1

        self.adj[v][w] = valor
        self.adj[w][v] = valor

        self.m += 1

    def removeA(
        self,
        v,
        w
    ):

        self._validar_vertice(v)
        self._validar_vertice(w)

        if not self._tem_aresta(v, w):
            return

        vazio = (
            None
            if self.ponderado
            else 0
        )

        self.adj[v][w] = vazio
        self.adj[w][v] = vazio

        self.m -= 1

    def degree(self, v):

        self._validar_vertice(v)

        return sum(
            1
            for w in range(self.n)
            if self._tem_aresta(v, w)
        )

    def connectivity_type(self):

        if self.n == 0:
            return 0

        visitados = self._alcancaveis(
            0
        )

        return int(
            len(visitados)
            != self.n
        )

    def is_connected(self):

        if self.n == 0:
            return True

        return (
            len(
                self._alcancaveis(0)
            )
            == self.n
        )

    def remove_vertex(self, v):

        self._validar_vertice(v)

        self.adj.pop(v)

        for linha in self.adj:
            linha.pop(v)

        novos_rotulos = {}

        for antigo_id, nome \
                in self.rotulos.items():

            if antigo_id == v:
                continue

            novo_id = (
                antigo_id - 1
                if antigo_id > v
                else antigo_id
            )
            novos_rotulos[
                novo_id
            ] = nome

        self.rotulos = novos_rotulos
        self.n -= 1
        self.m = sum(
            1
            for i in range(self.n)
            for j in range(
                i + 1,
                self.n
            )
            if self._tem_aresta(
                i,
                j
            )
        )

    removeV = remove_vertex
    removeVertice = remove_vertex

TGrafo = Grafo
TGrafoND = GrafoND