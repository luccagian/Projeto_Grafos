"""
Integrantes:
Gabriel Medina - 10426931
Gian Lucca Campanha Ribeiro - 10438361
Lucas Carmo - 10439830

Arquivo: visualizadorPyvis.py
Resumo: implementação da ferramenta PyVis para a visualização do grafo
"""


from pathlib import Path
from html import escape
import webbrowser

from pyvis.network import Network


# Cores aproximadas das linhas. Altere os códigos para ajustar o visual.
CORES_LINHAS = {
    "Linha 1-Azul": "#005CA9",
    "Linha 2-Verde": "#008061",
    "Linha 3-Vermelha": "#EE372F",
    "Linha 4-Amarela": "#FFD400",
    "Linha 5-Lilás": "#9B3894",
    "Linha 7-Rubi": "#9E005D",
    "Linha 8-Diamante": "#A8A9AD",
    "Linha 9-Esmeralda": "#00A88F",
    "Linha 10-Turquesa": "#00A6A8",
    "Linha 11-Coral": "#F0785A",
    "Linha 12-Safira": "#133C8D",
    "Linha 13-Jade": "#00A86B",
    "Linha 15-Prata": "#B5B8B9",
}
COR_PADRAO = "#808080"


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
        directed=grafo.direcionado,
        select_menu=False,
        filter_menu=False,
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
            f"Estação: {estacao}\n"
            f"{linha}\n"
            f"Vértice: {vertice}\n"
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
            color=CORES_LINHAS.get(linha, COR_PADRAO)
        )

    # Arestas

    quantidade_arestas = 0

    for origem in range(
        grafo.n
    ):

        for destino in range(
            0 if grafo.direcionado else origem + 1,
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
                    f"Integração / transferência\n"
                    f"{origem_nome}\n"
                    f"↕\n"
                    f"{destino_nome}"
                )

            else:

                titulo = (
                    f"{origem_nome}\n"
                    f"↔\n"
                    f"{destino_nome}\n"
                    f"Distância: {peso} km"
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

    # O seletor mostra nomes; o ID continua interno para localizar o nó.
    vertices = sorted(
        ((grafo.nome_vertice(i), i) for i in range(grafo.n)),
        key=lambda item: (item[0].casefold(), item[1]),
    )
    opcoes = "\n".join(
        f'<option value="{indice}">{escape(nome)}</option>'
        for nome, indice in vertices
    )
    seletor = f"""
    <div style="padding: 12px; font-family: sans-serif;">
      <label for="seletor-estacao">Selecionar estação: </label>
      <select id="seletor-estacao">
        <option value="">Escolha uma estação</option>
        {opcoes}
      </select>
    </div>
    """
    script = """
    <script>
      document.getElementById('seletor-estacao').addEventListener('change', function () {
        if (this.value === '') {
          network.unselectAll();
          return;
        }
        const id = Number(this.value);
        network.selectNodes([id]);
        network.focus(id, {scale: 1.5, animation: true});
      });
    </script>
    """
    html = caminho.read_text(encoding="utf-8")
    if "<body>" not in html or "</body>" not in html:
        raise ValueError("Não foi possível inserir o seletor no HTML gerado pelo PyVis.")
    html = html.replace("<body>", "<body>" + seletor, 1)
    html = html.replace("</body>", script + "</body>", 1)
    caminho.write_text(html, encoding="utf-8")

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