"""
Integrantes:
Gabriel Medina - 10426931
Gian Lucca Campanha Ribeiro - 10438361
Lucas Carmo - 10439830

Arquivo: analises.py
Resumo: técnicas da disciplina aplicadas ao grafo não orientado da rede
        metroferroviária (Parte 3 do projeto):
          - Item 1 (resiliência): pontos de articulação, pontes, ranking de
            estações pelo impacto da falha e rota alternativa;
          - Item 2 (características): graus, Euler, coloração, bipartição,
            condições para Hamilton, árvore geradora mínima e diâmetro.

Histórico de alterações:
    2026-11-19 | Gabriel Medina | Criação do arquivo com as análises da Parte 3.

Todas as funções recebem um GrafoND (matriz de adjacência) e não o
modificam. Para evitar varreduras O(n²) repetidas, a matriz é convertida uma
única vez em listas de adjacência por lista_de_adjacencia().
"""

from collections import Counter, deque
import heapq
import math


# ---------------------------------------------------------------------------
# Estruturas auxiliares
# ---------------------------------------------------------------------------

def lista_de_adjacencia(grafo):
    """Converte a matriz em lista de adjacência: lista[v] = [(w, peso), ...].

    Em grafos sem peso nas arestas, o peso de cada ligação é considerado 1.
    """
    lista = [[] for _ in range(grafo.n)]
    for v in range(grafo.n):
        for w in range(grafo.n):
            if grafo._tem_aresta(v, w):
                lista[v].append((w, grafo.adj[v][w]))
    return lista


def nome_estacao(rotulo):
    """Extrai o nome da estação de um rótulo no formato 'Estação | Linha'."""
    return rotulo.split("|", 1)[0].strip()


def nome_linha(rotulo):
    """Extrai a linha de um rótulo no formato 'Estação | Linha'."""
    partes = rotulo.split("|", 1)
    return partes[1].strip() if len(partes) > 1 else "(sem linha)"


def nomes_das_estacoes(grafo):
    """Retorna {nome_da_estação: [vértices estação-linha correspondentes]}."""
    estacoes = {}
    for v, rotulo in enumerate(grafo.rotulos):
        estacoes.setdefault(nome_estacao(rotulo).casefold(), []).append(v)
    return estacoes


def componentes(lista, excluidos=frozenset()):
    """Componentes conexas (BFS) ignorando os vértices em 'excluidos'."""
    visitados = set(excluidos)
    resultado = []
    for inicio in range(len(lista)):
        if inicio in visitados:
            continue
        componente = [inicio]
        visitados.add(inicio)
        fila = deque([inicio])
        while fila:
            atual = fila.popleft()
            for vizinho, _ in lista[atual]:
                if vizinho not in visitados:
                    visitados.add(vizinho)
                    componente.append(vizinho)
                    fila.append(vizinho)
        resultado.append(sorted(componente))
    return resultado


def dijkstra(lista, origem, excluidos=frozenset()):
    """Dijkstra a partir de 'origem' ignorando os vértices 'excluidos'.

    Retorna (distancias, anterior). Distância infinita indica vértice
    inalcançável. Exige pesos não negativos (válido para o estudo de caso).
    """
    distancias = [math.inf] * len(lista)
    anterior = [None] * len(lista)
    distancias[origem] = 0
    fila = [(0, origem)]
    while fila:
        distancia, atual = heapq.heappop(fila)
        if distancia > distancias[atual]:
            continue
        for vizinho, peso in lista[atual]:
            if vizinho in excluidos:
                continue
            nova = distancia + peso
            if nova < distancias[vizinho]:
                distancias[vizinho] = nova
                anterior[vizinho] = atual
                heapq.heappush(fila, (nova, vizinho))
    return distancias, anterior


def reconstruir_caminho(anterior, destino):
    """Reconstrói o caminho origem -> destino a partir do vetor 'anterior'."""
    caminho = []
    atual = destino
    while atual is not None:
        caminho.append(atual)
        atual = anterior[atual]
    return caminho[::-1]


# ---------------------------------------------------------------------------
# Item 1 - Investigação da resiliência da rede
# ---------------------------------------------------------------------------

def pontos_articulacao_e_pontes(grafo):
    """Pontos de articulação e pontes pelo algoritmo de Tarjan (DFS).

    Ponto de articulação: vértice cuja remoção aumenta o número de componentes.
    Ponte: aresta cuja remoção aumenta o número de componentes.
    Usa DFS iterativa (sem recursão) para não depender do limite do Python.

    Retorna (lista_de_articulações, lista_de_pontes) com pontes como (v, w), v < w.
    """
    lista = lista_de_adjacencia(grafo)
    n = grafo.n
    descoberta = [-1] * n
    low = [0] * n
    pai = [None] * n
    articulacoes = set()
    pontes = []
    tempo = 0

    for raiz in range(n):
        if descoberta[raiz] != -1:
            continue
        filhos_da_raiz = 0
        descoberta[raiz] = low[raiz] = tempo
        tempo += 1
        pilha = [(raiz, iter(lista[raiz]))]
        while pilha:
            v, vizinhos = pilha[-1]
            desceu = False
            for w, _ in vizinhos:
                if descoberta[w] == -1:
                    pai[w] = v
                    descoberta[w] = low[w] = tempo
                    tempo += 1
                    if v == raiz:
                        filhos_da_raiz += 1
                    pilha.append((w, iter(lista[w])))
                    desceu = True
                    break
                if w != pai[v]:
                    low[v] = min(low[v], descoberta[w])
            if desceu:
                continue
            pilha.pop()
            if pilha:
                p = pilha[-1][0]
                low[p] = min(low[p], low[v])
                if low[v] > descoberta[p]:
                    pontes.append((min(p, v), max(p, v)))
                if p != raiz and low[v] >= descoberta[p]:
                    articulacoes.add(p)
        if filhos_da_raiz > 1:
            articulacoes.add(raiz)

    return sorted(articulacoes), sorted(pontes)


def ranking_falhas_estacoes(grafo):
    """Simula a falha de cada estação física e ordena pelo impacto estrutural.

    Para cada nome de estação, todas as representações estação-linha são
    removidas. Mede-se: número de componentes restantes, tamanho da maior
    componente e quantidade de vértices desconectados dela.

    Retorna lista de dicts ordenada do maior para o menor impacto.
    """
    lista = lista_de_adjacencia(grafo)
    base = len(componentes(lista))
    resultado = []
    for chave, vertices in nomes_das_estacoes(grafo).items():
        restantes = componentes(lista, excluidos=frozenset(vertices))
        maior = max((len(c) for c in restantes), default=0)
        total = sum(len(c) for c in restantes)
        resultado.append({
            "estacao": nome_estacao(grafo.rotulos[vertices[0]]),
            "vertices": vertices,
            "componentes": len(restantes),
            "maior_componente": maior,
            "desconectados": total - maior,
            "critica": len(restantes) > base,
        })
    resultado.sort(key=lambda r: (-r["desconectados"], -r["componentes"], r["estacao"]))
    return resultado


def rota_alternativa(grafo, origem, destino, vertice_falha):
    """Compara a rota normal com a rota sem a estação do 'vertice_falha'.

    Retorna dict com a distância/caminho originais, a distância/caminho
    alternativos (None se a falha desconecta origem e destino) e a lista de
    vértices desativados. Levanta ValueError se origem ou destino pertencerem
    à estação indisponível.
    """
    grafo._validar_vertice(origem)
    grafo._validar_vertice(destino)
    grafo._validar_vertice(vertice_falha)
    nome = nome_estacao(grafo.rotulos[vertice_falha])
    desativados = nomes_das_estacoes(grafo)[nome.casefold()]
    if origem in desativados or destino in desativados:
        raise ValueError("Origem ou destino pertence à estação indisponível.")

    lista = lista_de_adjacencia(grafo)
    dist, ant = dijkstra(lista, origem)
    dist_falha, ant_falha = dijkstra(lista, origem, frozenset(desativados))

    resultado = {
        "estacao_falha": nome,
        "desativados": desativados,
        "distancia_original": dist[destino],
        "caminho_original": reconstruir_caminho(ant, destino) if dist[destino] != math.inf else [],
        "distancia_alternativa": None,
        "caminho_alternativo": [],
    }
    if dist_falha[destino] != math.inf:
        resultado["distancia_alternativa"] = dist_falha[destino]
        resultado["caminho_alternativo"] = reconstruir_caminho(ant_falha, destino)
    return resultado


# ---------------------------------------------------------------------------
# Item 2 - Características do grafo
# ---------------------------------------------------------------------------

def estatisticas_graus(grafo):
    """Distribuição de graus: mínimo, máximo, média e vértices de maior grau."""
    graus = [grafo.degree(v) for v in range(grafo.n)]
    if not graus:
        return {"minimo": 0, "maximo": 0, "media": 0.0, "distribuicao": {}, "maior_grau": []}
    maximo = max(graus)
    return {
        "minimo": min(graus),
        "maximo": maximo,
        "media": sum(graus) / grafo.n,
        "distribuicao": dict(sorted(Counter(graus).items())),
        "maior_grau": [v for v, g in enumerate(graus) if g == maximo],
    }


def analise_euleriana(grafo):
    """Teorema de Euler: ciclo euleriano (todos os graus pares), percurso
    euleriano (exatamente dois graus ímpares) ou nenhum, se o grafo é conexo."""
    impares = [v for v in range(grafo.n) if grafo.degree(v) % 2 == 1]
    conexo = grafo.is_connected()
    if not conexo:
        tipo = "nenhum"
    elif not impares:
        tipo = "ciclo"
    elif len(impares) == 2:
        tipo = "percurso"
    else:
        tipo = "nenhum"
    return {"conexo": conexo, "vertices_grau_impar": impares, "tipo": tipo}


def eh_bipartido(grafo):
    """Verifica se o grafo é bipartido por 2-coloração em BFS."""
    lista = lista_de_adjacencia(grafo)
    lado = [None] * grafo.n
    for inicio in range(grafo.n):
        if lado[inicio] is not None:
            continue
        lado[inicio] = 0
        fila = deque([inicio])
        while fila:
            atual = fila.popleft()
            for vizinho, _ in lista[atual]:
                if lado[vizinho] is None:
                    lado[vizinho] = 1 - lado[atual]
                    fila.append(vizinho)
                elif lado[vizinho] == lado[atual]:
                    return False
    return True


def coloracao_welsh_powell(grafo):
    """Coloração própria pelo algoritmo de Welsh-Powell.

    Ordena os vértices por grau decrescente e preenche uma cor por vez com
    vértices não adjacentes. O número de cores é um limite superior para o
    número cromático. Retorna (quantidade_de_cores, vetor_de_cores 1..k).
    """
    lista = lista_de_adjacencia(grafo)
    vizinhos = [{w for w, _ in lista[v]} for v in range(grafo.n)]
    ordem = sorted(range(grafo.n), key=lambda v: (-len(vizinhos[v]), v))
    cores = [None] * grafo.n
    cor = 0
    pendentes = ordem
    while pendentes:
        cor += 1
        da_cor = set()
        for v in pendentes:
            if not (vizinhos[v] & da_cor):
                cores[v] = cor
                da_cor.add(v)
        pendentes = [v for v in pendentes if cores[v] is None]
    return cor, cores


def clique_maxima(grafo):
    """Tamanho da maior clique (Bron-Kerbosch com pivô); limite inferior do
    número cromático. Adequado a grafos esparsos como o da rede."""
    lista = lista_de_adjacencia(grafo)
    vizinhos = [{w for w, _ in lista[v]} for v in range(grafo.n)]
    melhor = [[]]

    def expandir(r, p, x):
        if not p and not x:
            if len(r) > len(melhor[0]):
                melhor[0] = list(r)
            return
        pivo = max(p | x, key=lambda u: len(vizinhos[u] & p))
        for v in list(p - vizinhos[pivo]):
            expandir(r + [v], p & vizinhos[v], x & vizinhos[v])
            p.remove(v)
            x.add(v)

    expandir([], set(range(grafo.n)), set())
    return len(melhor[0]), melhor[0]


def condicoes_hamiltoniano(grafo):
    """Testa condições NECESSÁRIAS para ciclo e caminho hamiltonianos.

    Decidir Hamilton é um problema NP-completo; por isso são aplicadas
    condições necessárias que, quando violadas, provam a inexistência:
      ciclo   -> grafo conexo, todos os graus >= 2 e nenhum ponto de articulação;
      caminho -> grafo conexo, no máximo 2 vértices de grau 1 e nenhum vértice
                 cuja remoção deixe 3 ou mais componentes.
    Se nenhuma condição for violada o resultado é 'inconclusivo'.
    """
    n = grafo.n
    lista = lista_de_adjacencia(grafo)
    conexo = len(componentes(lista)) <= 1
    articulacoes, _ = pontos_articulacao_e_pontes(grafo)
    grau_1 = [v for v in range(n) if len(lista[v]) == 1]
    grau_0 = [v for v in range(n) if len(lista[v]) == 0]

    motivos_ciclo = []
    if n < 3:
        motivos_ciclo.append("o grafo tem menos de 3 vértices")
    if not conexo:
        motivos_ciclo.append("o grafo é desconexo")
    if grau_1 or grau_0:
        motivos_ciclo.append(f"existem {len(grau_1) + len(grau_0)} vértices com grau menor que 2")
    if articulacoes:
        motivos_ciclo.append(f"existem {len(articulacoes)} pontos de articulação")

    motivos_caminho = []
    if not conexo:
        motivos_caminho.append("o grafo é desconexo")
    if len(grau_1) > 2:
        motivos_caminho.append(f"existem {len(grau_1)} vértices de grau 1 (máximo permitido: 2)")
    corte_forte = [
        v for v in articulacoes
        if len(componentes(lista, excluidos=frozenset([v]))) >= 3
    ]
    if corte_forte:
        motivos_caminho.append(
            f"{len(corte_forte)} vértices deixam 3 ou mais componentes ao serem removidos"
        )

    return {
        "ciclo": "não admite" if motivos_ciclo else "inconclusivo",
        "motivos_ciclo": motivos_ciclo,
        "caminho": "não admite" if motivos_caminho else "inconclusivo",
        "motivos_caminho": motivos_caminho,
    }


def arvore_geradora_minima(grafo):
    """Árvore (ou floresta) geradora mínima pelo algoritmo de Kruskal.

    Retorna (peso_total, arestas_da_árvore, peso_total_do_grafo). As arestas
    fora da árvore são os trechos redundantes (formam ciclos na rede).
    """
    arestas = sorted(
        ((grafo.adj[v][w], v, w)
         for v in range(grafo.n) for w in range(v + 1, grafo.n)
         if grafo._tem_aresta(v, w)),
        key=lambda a: (a[0], a[1], a[2]),
    )
    representante = list(range(grafo.n))

    def achar(x):
        while representante[x] != x:
            representante[x] = representante[representante[x]]
            x = representante[x]
        return x

    escolhidas = []
    total = 0.0
    for peso, v, w in arestas:
        rv, rw = achar(v), achar(w)
        if rv != rw:
            representante[rv] = rw
            escolhidas.append((v, w, peso))
            total += peso
    return total, escolhidas, sum(a[0] for a in arestas)


def diametro_e_raio(grafo):
    """Excentricidades (Dijkstra a partir de cada vértice).

    Diâmetro = maior distância mínima entre dois vértices; raio = menor
    excentricidade. Só são definidos para grafo conexo (caso contrário o
    diâmetro considera apenas pares alcançáveis e o raio é None).
    """
    lista = lista_de_adjacencia(grafo)
    excentricidades = []
    melhor_par = (0, None, None)
    for v in range(grafo.n):
        dist, _ = dijkstra(lista, v)
        finitas = [(d, w) for w, d in enumerate(dist) if d != math.inf]
        d_max, w_max = max(finitas)
        excentricidades.append(d_max)
        if d_max > melhor_par[0]:
            melhor_par = (d_max, v, w_max)
    conexo = len(componentes(lista)) <= 1
    raio = min(excentricidades) if conexo and excentricidades else None
    centro = excentricidades.index(raio) if raio is not None else None
    return {
        "conexo": conexo,
        "diametro": melhor_par[0],
        "extremos": (melhor_par[1], melhor_par[2]),
        "raio": raio,
        "centro": centro,
    }
