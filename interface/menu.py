"""
Integrantes:
Gabriel Medina - 10426931
Gian Lucca Campanha Ribeiro - 10438361
Lucas Carmo - 10439830

Arquivo: menu.py
Resumo: menu principal do projeto de resiliência da rede metroferroviária.

Histórico de alterações:
    2026-10-28 | Gian Lucca Campanha Ribeiro | Refatoração da estrutura do projeto em pastas.
    2026-10-28 | Gian Lucca Campanha Ribeiro | Refatoração, visualização PyVis e pesos em km (Haversine).
    2026-11-19 | Gabriel Medina | Inclusão das opções n e o (Parte 3) e do histórico no cabeçalho.
"""

from pathlib import Path

from interface import acoes_menu as acoes

ARQUIVO_PADRAO = Path(__file__).resolve().parent.parent / "dados" / "grafo.txt"
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
    print("m) Visualizar grafo completo - PyVis")
    print("n) Investigar resiliência da rede (Parte 3 - item 1)")
    print("o) Analisar características do grafo (Parte 3 - item 2)")


def exigir_grafo(grafo):
    if grafo is None:
        print("\n[AVISO] Primeiro carregue o grafo usando a opção 'a'.")
        return False
    return True


def menu(caminho: Path = ARQUIVO_PADRAO) -> None:
    grafo = None

    while True:
        exibir_cabecalho()
        exibir_menu()
        opcao = input("\nEscolha uma opção: ").strip().lower()

        try:
            if opcao == "a":
                grafo = acoes.ler_grafo(caminho)

            elif opcao == "b":
                if exigir_grafo(grafo):
                    acoes.gravar_grafo(grafo, caminho)

            elif opcao == "c":
                if exigir_grafo(grafo):
                    acoes.inserir_vertice(grafo)

            elif opcao == "d":
                if exigir_grafo(grafo):
                    acoes.inserir_aresta(grafo)

            elif opcao == "e":
                if exigir_grafo(grafo):
                    acoes.remover_vertice(grafo)

            elif opcao == "f":
                if exigir_grafo(grafo):
                    acoes.remover_aresta(grafo)

            elif opcao == "g":
                acoes.mostrar_conteudo_arquivo(caminho)

            elif opcao == "h":
                if exigir_grafo(grafo):
                    acoes.mostrar_grafo(grafo)

            elif opcao == "i":
                if exigir_grafo(grafo):
                    acoes.mostrar_conexidade(grafo)

            elif opcao == "j":
                print("\nAplicação encerrada.")
                break

            elif opcao == "k":
                if exigir_grafo(grafo):
                    acoes.mostrar_caminho_minimo(grafo)

            elif opcao == "l":
                if exigir_grafo(grafo):
                    acoes.simular_falha_estacao(grafo)

            elif opcao == "m":
                if exigir_grafo(grafo):
                    acoes.visualizar(grafo)

            elif opcao == "n":
                if exigir_grafo(grafo):
                    acoes.investigar_resiliencia(grafo)

            elif opcao == "o":
                if exigir_grafo(grafo):
                    acoes.analisar_caracteristicas(grafo)

            else:
                print("\n[ERRO] Opção inválida. Escolha uma letra entre 'a' e 'o'.")

        except (ValueError, IndexError, OSError) as erro:
            print(f"\n[ERRO] {erro}")
