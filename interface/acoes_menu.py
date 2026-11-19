"""
Integrantes:
Gabriel Medina - 10426931
Gian Lucca Campanha Ribeiro - 10438361
Lucas Carmo - 10439830

Arquivo: acoes_menu.py
Resumo: ações das opções do menu do projeto.

Histórico de alterações:
    2026-10-01 | Gian Lucca Campanha Ribeiro | Adição do arquivo ao repositório (upload).
    2026-10-26 | Gian Lucca Campanha Ribeiro | Semi-refatoração da estrutura do projeto.
    2026-10-28 | Gian Lucca Campanha Ribeiro | Refatoração da estrutura do projeto em pastas.
    2026-10-28 | Gian Lucca Campanha Ribeiro | Refatoração, visualização PyVis e pesos em km (Haversine).
    2026-11-19 | Gabriel Medina | Inclusão das ações de resiliência e características do grafo (Parte 3).
"""

from pathlib import Path

from grafos import analises
from grafos.grafoMatriz import Grafo, GrafoND


def ler_grafo(caminho: Path):
    grafo = Grafo.from_file(caminho)
    classe = "orientado" if grafo.direcionado else "não orientado"
    print(
        f"\n[SUCESSO] Grafo carregado: {grafo.n} vértices, "
        f"{grafo.m} arestas, tipo {grafo.tipo_grafo} ({classe})."
    )
    return grafo


def gravar_grafo(grafo, caminho: Path) -> None:
    grafo.to_file(caminho)
    print(f"\n[SUCESSO] Grafo gravado em '{caminho}'.")


def inserir_vertice(grafo) -> None:
    rotulo = input("Nome/rótulo do novo vértice: ").strip()

    peso = None
    if grafo.peso_no_vertice:
        peso = float(input("Peso do vértice: "))

    indice = grafo.inserir_vertice(rotulo, peso)
    print(f"\n[SUCESSO] Vértice {indice} ('{rotulo}') inserido.")


def inserir_aresta(grafo) -> None:
    origem = int(input("Vértice de origem: "))
    destino = int(input("Vértice de destino: "))

    peso = None
    if grafo.peso_na_aresta:
        peso = float(input("Peso da aresta: "))

    grafo.insereA(origem, destino, peso)

    if isinstance(grafo, GrafoND):
        representacao = f"{{{origem}, {destino}}}"
    else:
        representacao = f"{origem} -> {destino}"

    print(f"\n[SUCESSO] Aresta {representacao} inserida.")


def remover_vertice(grafo) -> None:
    vertice = int(input(f"Vértice a remover (0 a {grafo.n - 1}): "))
    rotulo = grafo.rotulos[vertice]
    grafo.remove_vertex(vertice)
    print(f"\n[SUCESSO] Vértice {vertice} ('{rotulo}') removido com suas arestas.")


def remover_aresta(grafo) -> None:
    origem = int(input("Primeiro vértice: "))
    destino = int(input("Segundo vértice: "))
    grafo.removeA(origem, destino)
    print(f"\n[SUCESSO] Aresta entre {origem} e {destino} removida.")


def mostrar_conteudo_arquivo(caminho: Path) -> None:
    print(f"\n--- Conteúdo atual de {caminho} ---")
    print(caminho.read_text(encoding="utf-8"))


def mostrar_grafo(grafo) -> None:
    print("\n--- Representação do grafo ---")
    grafo.show()


def mostrar_caminho_minimo(grafo) -> None:
    origem = int(input(f"Vértice de origem (0 a {grafo.n - 1}): "))
    destino = int(input(f"Vértice de destino (0 a {grafo.n - 1}): "))

    distancia, caminho = grafo.caminho_minimo(origem, destino)

    if not caminho:
        print("\n[RESULTADO] Não existe caminho entre os vértices informados.")
        return

    print("\n--- Caminho mínimo (Dijkstra) ---")
    for i, vertice in enumerate(caminho):
        print(f"{vertice:3d} - {grafo.rotulos[vertice]}")
        if i < len(caminho) - 1:
            proximo = caminho[i + 1]
            peso = grafo.adj[vertice][proximo]
            print(f"      | {float(peso):.3f} km")
            print("      v")

    print(f"Distância total aproximada: {distancia:.3f} km")


def simular_falha_estacao(grafo) -> None:
    if not isinstance(grafo, GrafoND):
        raise ValueError(
            "A simulação de falha de estação desta aplicação foi definida "
            "para o grafo não orientado do estudo de caso."
        )

    vertice = int(input(f"Vértice da estação indisponível (0 a {grafo.n - 1}): "))
    resultado = grafo.simular_falha_estacao(vertice)

    print("\n--- Simulação de falha de estação ---")
    print(f"Estação: {resultado['nome']}")
    ids = resultado["vertices_indisponiveis"]
    print("Vértices estação-linha desativados: " + ", ".join(map(str, ids)))

    componentes = resultado["componentes_depois"]
    if resultado["continua_conexo"]:
        print("Resultado: a rede restante continua CONEXA.")
    else:
        print(f"Resultado: a rede ficou DESCONEXA em {len(componentes)} componentes.")
        tamanhos = sorted((len(c) for c in componentes), reverse=True)
        print("Tamanho das componentes: " + ", ".join(map(str, tamanhos)))

    if resultado["falha_critica"]:
        print("Classificação: falha estruturalmente crítica (aumenta o número de componentes).")
    else:
        print("Classificação: a remoção não aumenta o número de componentes da rede.")


def mostrar_conexidade(grafo) -> None:
    print("\n--- Análise de conexidade ---")

    if isinstance(grafo, GrafoND):
        estado = "CONEXO" if grafo.is_connected() else "DESCONEXO"
        print(f"Grafo não orientado: {estado}")
        print(
            "Grafo reduzido/FCONEX não se aplica ao modelo não orientado "
            "adotado neste projeto."
        )
        return

    categoria = grafo.categoria_conexidade()
    descricoes = {
        3: "C3 - fortemente conexo",
        2: "C2 - unilateralmente conexo",
        1: "C1 - fracamente conexo",
        0: "C0 - desconexo",
    }
    print(f"Categoria: {descricoes[categoria]}")

    reduzido = grafo.grafo_reduzido()
    print(
        f"Grafo reduzido: {reduzido.n} vértices/componentes e "
        f"{reduzido.m} arestas."
    )
    reduzido.show()


# ---------------------------------------------------------------------------
# Parte 3 - Item 1: investigação da resiliência da rede
# ---------------------------------------------------------------------------

def exigir_nao_orientado(grafo) -> None:
    if not isinstance(grafo, GrafoND):
        raise ValueError(
            "As análises da Parte 3 foram definidas para o grafo não orientado "
            "do estudo de caso."
        )


def formatar_vertice(grafo, vertice: int) -> str:
    return f"{vertice:3d} - {grafo.rotulos[vertice]}"


def formatar_rota(grafo, caminho) -> str:
    """Lista os nomes das estações do caminho, juntando as integrações
    (vértices consecutivos da mesma estação) em um único nome."""
    nomes = []
    for v in caminho:
        nome = analises.nome_estacao(grafo.rotulos[v])
        if not nomes or nomes[-1] != nome:
            nomes.append(nome)
    return " -> ".join(nomes)


def mostrar_pontos_articulacao(grafo) -> None:
    articulacoes, _ = analises.pontos_articulacao_e_pontes(grafo)
    por_linha = {}
    for v in articulacoes:
        linha = analises.nome_linha(grafo.rotulos[v])
        por_linha.setdefault(linha, []).append(analises.nome_estacao(grafo.rotulos[v]))

    print("\n--- Estações críticas: pontos de articulação (Tarjan) ---")
    print(f"{len(articulacoes)} de {grafo.n} vértices estação-linha são pontos de articulação.")
    print("A indisponibilidade de qualquer um deles separa a rede em mais componentes.\n")
    for linha in sorted(por_linha):
        print(f"{linha} ({len(por_linha[linha])}): " + ", ".join(por_linha[linha]))


def mostrar_pontes(grafo) -> None:
    _, pontes = analises.pontos_articulacao_e_pontes(grafo)
    trechos = [(grafo.adj[v][w], v, w) for v, w in pontes if grafo.adj[v][w] > 0]
    integracoes = len(pontes) - len(trechos)

    print("\n--- Trechos críticos: pontes ---")
    print(f"{len(pontes)} de {grafo.m} arestas são pontes "
          f"({len(trechos)} trechos entre estações e {integracoes} integrações).")
    print("Sem caminho alternativo: se uma ponte for interrompida, a rede é dividida.")
    print("\nCinco trechos-ponte mais longos:")
    for peso, v, w in sorted(trechos, reverse=True)[:5]:
        print(f"  {float(peso):7.3f} km | {grafo.rotulos[v]}  <->  {grafo.rotulos[w]}")


def mostrar_ranking_falhas(grafo) -> None:
    ranking = analises.ranking_falhas_estacoes(grafo)
    criticas = sum(1 for r in ranking if r["critica"])

    print("\n--- Ranking de estações pelo impacto da falha ---")
    print(f"{criticas} de {len(ranking)} estações, quando indisponíveis, dividem a rede.\n")
    print(f"{'Estação':32s} {'Componentes':>11s} {'Maior comp.':>11s} {'Isolados':>9s}")
    for r in ranking[:10]:
        print(f"{r['estacao'][:32]:32s} {r['componentes']:11d} "
              f"{r['maior_componente']:11d} {r['desconectados']:9d}")
    print("\n'Isolados' = vértices que deixam de alcançar a maior componente da rede.")


def mostrar_rota_alternativa(grafo) -> None:
    origem = int(input(f"Vértice de origem (0 a {grafo.n - 1}): "))
    destino = int(input(f"Vértice de destino (0 a {grafo.n - 1}): "))
    falha = int(input(f"Vértice da estação indisponível (0 a {grafo.n - 1}): "))

    r = analises.rota_alternativa(grafo, origem, destino, falha)

    print(f"\n--- Rota alternativa com a estação {r['estacao_falha']} indisponível ---")
    if not r["caminho_original"]:
        print("[RESULTADO] Não existe caminho entre os vértices informados na rede original.")
        return

    print(f"Rota original: {r['distancia_original']:.3f} km")
    print("  " + formatar_rota(grafo, r["caminho_original"]))

    if r["distancia_alternativa"] is None:
        print("\n[RESULTADO] Sem rota alternativa: a falha desconecta origem e destino.")
        return

    if r["caminho_alternativo"] == r["caminho_original"]:
        print("\n[RESULTADO] A estação indisponível não faz parte da rota original; nada muda.")
        return

    acrescimo = r["distancia_alternativa"] - r["distancia_original"]
    print(f"\nRota alternativa: {r['distancia_alternativa']:.3f} km (+{acrescimo:.3f} km)")
    print("  " + formatar_rota(grafo, r["caminho_alternativo"]))


def investigar_resiliencia(grafo) -> None:
    exigir_nao_orientado(grafo)
    opcoes = {
        "1": mostrar_pontos_articulacao,
        "2": mostrar_pontes,
        "3": mostrar_ranking_falhas,
        "4": mostrar_rota_alternativa,
    }
    while True:
        print("\n--- Investigação de resiliência da rede ---")
        print("1) Estações críticas (pontos de articulação)")
        print("2) Trechos críticos (pontes)")
        print("3) Ranking de estações pelo impacto da falha")
        print("4) Rota alternativa com estação indisponível")
        print("0) Voltar ao menu principal")
        escolha = input("Escolha uma análise: ").strip()
        if escolha == "0":
            return
        if escolha not in opcoes:
            print("\n[ERRO] Opção inválida. Escolha de 0 a 4.")
            continue
        try:
            opcoes[escolha](grafo)
        except (ValueError, IndexError) as erro:
            print(f"\n[ERRO] {erro}")


# ---------------------------------------------------------------------------
# Parte 3 - Item 2: características do problema modelado
# ---------------------------------------------------------------------------

def analisar_caracteristicas(grafo) -> None:
    exigir_nao_orientado(grafo)
    print("\n--- Características do grafo ---")

    # 1) Graus
    graus = analises.estatisticas_graus(grafo)
    print("\n1) Graus dos vértices")
    print(f"   mínimo {graus['minimo']} | máximo {graus['maximo']} | média {graus['media']:.2f}")
    print("   distribuição: " + "; ".join(
        f"grau {g}: {q} vértice(s)" for g, q in graus["distribuicao"].items()))
    for v in graus["maior_grau"]:
        print(f"   maior grau: {formatar_vertice(grafo, v)}")

    # 2) Euler
    euler = analises.analise_euleriana(grafo)
    print("\n2) Grafo euleriano (Teorema de Euler)")
    print(f"   vértices de grau ímpar: {len(euler['vertices_grau_impar'])}")
    descricao = {
        "ciclo": "possui ciclo euleriano (grafo euleriano)",
        "percurso": "possui percurso euleriano, mas não ciclo",
        "nenhum": "não possui ciclo nem percurso euleriano",
    }
    print(f"   resultado: o grafo {descricao[euler['tipo']]}.")

    # 3) Coloração e bipartição
    cores, _ = analises.coloracao_welsh_powell(grafo)
    tamanho_clique, _ = analises.clique_maxima(grafo)
    bipartido = analises.eh_bipartido(grafo)
    print("\n3) Coloração (Welsh-Powell)")
    print(f"   cores usadas (limite superior): {cores} | maior clique (limite inferior): {tamanho_clique}")
    if cores == tamanho_clique:
        print(f"   número cromático exato: {cores}")
    else:
        print(f"   número cromático entre {tamanho_clique} e {cores}")
    print(f"   grafo bipartido: {'sim' if bipartido else 'não'}")

    # 4) Hamilton
    ham = analises.condicoes_hamiltoniano(grafo)
    print("\n4) Grafo hamiltoniano (condições necessárias)")
    print(f"   ciclo hamiltoniano: {ham['ciclo']}")
    for motivo in ham["motivos_ciclo"]:
        print(f"     - {motivo}")
    print(f"   caminho hamiltoniano: {ham['caminho']}")
    for motivo in ham["motivos_caminho"]:
        print(f"     - {motivo}")

    # 5) Árvore geradora mínima
    peso_agm, arestas_agm, peso_total = analises.arvore_geradora_minima(grafo)
    print("\n5) Árvore geradora mínima (Kruskal)")
    print(f"   peso da árvore: {peso_agm:.3f} km de {peso_total:.3f} km da rede "
          f"({len(arestas_agm)} arestas)")
    print(f"   trechos redundantes (fora da árvore): {grafo.m - len(arestas_agm)}")

    # 6) Diâmetro e raio
    medidas = analises.diametro_e_raio(grafo)
    print("\n6) Diâmetro e raio (Dijkstra a partir de cada vértice)")
    origem, destino = medidas["extremos"]
    print(f"   diâmetro: {medidas['diametro']:.3f} km")
    print(f"     entre {formatar_vertice(grafo, origem)}")
    print(f"       e   {formatar_vertice(grafo, destino)}")
    if medidas["raio"] is not None:
        print(f"   raio: {medidas['raio']:.3f} km | centro: {formatar_vertice(grafo, medidas['centro'])}")
    else:
        print("   raio não definido: o grafo é desconexo.")


def visualizar(grafo) -> None:
    try:
        from visualizacao.visualizadorPyvis import visualizar_grafo
        visualizar_grafo(grafo, arquivo_saida="grafo_completo.html")
    except ModuleNotFoundError as erro:
        if erro.name != "pyvis":
            raise
        print("\n[ERRO] Instale o PyVis: python -m pip install -r requirements.txt")
