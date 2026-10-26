"""
Integrantes:
Gabriel Medina - 10426931
Gian Lucca Campanha Ribeiro - 10438361
Lucas Carmo - 10439830

Arquivo: visualizadorPyvis.py
Resumo: implementação da ferramenta PyVis para a visualização do grafo
"""


from pathlib import Path
import webbrowser

from pyvis.network import Network


def extrair_linha(nome):
    """
    Recebe, por exemplo:

    Luz | Linha 1-Azul

    Retorna:

    Linha 1-Azul
    """

    if "|" not in nome:
        return ""

    partes = nome.split(
        "|",
        1
    )

    return partes[1].strip()


def extrair_estacao(nome):
    """
    Luz | Linha 1-Azul -> Luz
    """

    if "|" not in nome:
        return nome.strip()

    return nome.split(
        "|",
        1
    )[0].strip()


def visualizar_grafo(
    grafo,
    arquivo_saida="grafo_completo.html"
):

    if grafo is None:
        raise ValueError(
            "Nenhum grafo carregado."
        )

    rede = Network(
        height="900px",
        width="100%",
        bgcolor="#101418",
        font_color="white",
        directed=False,
        select_menu=True,
        filter_menu=True,
        cdn_resources="in_line"
    )

    # Configuração da física

    rede.barnes_hut(
        gravity=-10000,
        central_gravity=0.15,
        spring_length=110,
        spring_strength=0.015,
        damping=0.09,
        overlap=0
    )

    # Vértices

    for vertice in range(
        grafo.n
    ):

        nome_completo = (
            grafo.nome_vertice(
                vertice
            )
        )

        estacao = extrair_estacao(
            nome_completo
        )

        linha = extrair_linha(
            nome_completo
        )

        grau = grafo.degree(
            vertice
        )

        titulo = (
            f"<b>{estacao}</b><br>"
            f"{linha}<br>"
            f"Vértice: {vertice}<br>"
            f"Grau: {grau}"
        )

        rede.add_node(
            vertice,
            label=estacao,
            title=titulo,
            size=(
                12
                + min(
                    grau * 2,
                    30
                )
            ),
            group=linha
        )

    # Arestas

    quantidade_arestas = 0

    for origem in range(
        grafo.n
    ):

        for destino in range(
            origem + 1,
            grafo.n
        ):

            if not grafo._tem_aresta(
                origem,
                destino
            ):
                continue

            peso = (
                grafo.adj[
                    origem
                ][
                    destino
                ]
            )

            origem_nome = (
                grafo.nome_vertice(
                    origem
                )
            )

            destino_nome = (
                grafo.nome_vertice(
                    destino
                )
            )

            if peso == 0:

                titulo = (
                    f"<b>Integração / "
                    f"transferência</b><br>"
                    f"{origem_nome}<br>"
                    f"↕<br>"
                    f"{destino_nome}"
                )

            else:

                titulo = (
                    f"{origem_nome}"
                    f"<br>↔<br>"
                    f"{destino_nome}"
                    f"<br>"
                    f"Distância: "
                    f"{peso} km"
                )

            rede.add_edge(
                origem,
                destino,
                title=titulo,
                value=1
            )

            quantidade_arestas += 1

    # Opções

    rede.set_options("""
    {
      "nodes": {
        "borderWidth": 2,
        "font": {
          "size": 13
        }
      },

      "edges": {
        "smooth": false,
        "font": {
          "size": 10
        }
      },

      "interaction": {
        "hover": true,
        "navigationButtons": true,
        "keyboard": true,
        "multiselect": true
      },

      "physics": {
        "enabled": true,
        "stabilization": {
          "enabled": true,
          "iterations": 1000,
          "updateInterval": 50
        }
      }
    }
    """)

    caminho = Path(
        arquivo_saida
    ).resolve()

    rede.write_html(
        str(caminho),
        open_browser=False
    )

    print(
        "\n========================================"
    )
    print(
        "       VISUALIZAÇÃO PYVIS"
    )
    print(
        "========================================"
    )
    print(
        f"Vértices: {grafo.n}"
    )
    print(
        f"Arestas: "
        f"{quantidade_arestas}"
    )
    print(
        f"Arquivo: {caminho}"
    )
    print(
        "========================================"
    )

    webbrowser.open(
        caminho.as_uri()
    )

    return str(caminho)