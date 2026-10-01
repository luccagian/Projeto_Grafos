# -*- coding: utf-8 -*-
"""
Integrantes:
Gabriel Medina - 10426931
Gian Lucca Campanha Ribeiro - 10438361
Lucas Carmo - 10439830

Arquivo: menu.py
Resumo: menu principal do projeto de resiliência da rede metroferroviária.
"""

from pathlib import Path

from grafoMatriz import Grafo, GrafoND


ARQUIVO_PADRAO = Path("grafo.txt")
TITULO = "RESILIÊNCIA DA REDE METROFERROVIÁRIA DE SÃO PAULO E REGIÃO METROPOLITANA"


def exibir_cabecalho() -> None:
    print("\n" + "=" * 72)
    print(TITULO.center(72))
    print("=" * 72)


def exibir_menu() -> None:
    print("a) Ler dados do arquivo grafo.txt")
    print("b) Gravar dados no arquivo grafo.txt")
    print("c) Inserir vértice")
    print("d) Inserir aresta")
    print("e) Remover vértice")
    print("f) Remover aresta")
    print("g) Mostrar conteúdo do arquivo")
    print("h) Mostrar grafo")
    print("i) Apresentar conexidade")
    print("j) Encerrar a aplicação")
    print("k) Calcular caminho mínimo entre duas estações")
    print("l) Simular falha de uma estação")


def exigir_grafo(grafo):
    if grafo is None:
        print("\n[AVISO] Primeiro carregue o grafo usando a opção 'a'.")
        return False
    return True


def ler_grafo(caminho: Path):
    grafo = Grafo.from_file(caminho)
    classe = "orientado" if grafo.direcionado else "não orientado"
    print(
        f"\n[SUCESSO] Grafo carregado: {grafo.n} vértices, "
        f"{grafo.m} arestas, tipo {grafo.tipo_grafo} ({classe})."
    )
    return grafo


def gravar_grafo(grafo, caminho: Path) -> None:
    grafo.salvar_arquivo(caminho)
    print(f"\n[SUCESSO] Grafo gravado em '{caminho}")


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
    grafo.mostrar_lista_adjacencia()


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
        estado = "CONEXO" if grafo.eh_conexo() else "DESCONEXO"
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
    reduzido.mostrar_lista_adjacencia()


def menu(caminho: Path = ARQUIVO_PADRAO) -> None:
    grafo = None

    while True:
        exibir_cabecalho()
        exibir_menu()
        opcao = input("\nEscolha uma opção: ").strip().lower()

        try:
            if opcao == "a":
                grafo = ler_grafo(caminho)

            elif opcao == "b":
                if exigir_grafo(grafo):
                    gravar_grafo(grafo, caminho)

            elif opcao == "c":
                if exigir_grafo(grafo):
                    inserir_vertice(grafo)

            elif opcao == "d":
                if exigir_grafo(grafo):
                    inserir_aresta(grafo)

            elif opcao == "e":
                if exigir_grafo(grafo):
                    remover_vertice(grafo)

            elif opcao == "f":
                if exigir_grafo(grafo):
                    remover_aresta(grafo)

            elif opcao == "g":
                mostrar_conteudo_arquivo(caminho)

            elif opcao == "h":
                if exigir_grafo(grafo):
                    mostrar_grafo(grafo)

            elif opcao == "i":
                if exigir_grafo(grafo):
                    mostrar_conexidade(grafo)

            elif opcao == "j":
                print("\nAplicação encerrada.")
                break

            elif opcao == "k":
                if exigir_grafo(grafo):
                    mostrar_caminho_minimo(grafo)

            elif opcao == "l":
                if exigir_grafo(grafo):
                    simular_falha_estacao(grafo)

            else:
                print("\n[ERRO] Opção inválida. Escolha uma letra entre 'a' e 'l'.")

        except (ValueError, IndexError, OSError) as erro:
            print(f"\n[ERRO] {erro}")


if __name__ == "__main__":
    menu()
