"""
Integrantes:
Gabriel Medina - 10426931
Gian Lucca Campanha Ribeiro - 10438361
Lucas Carmo - 10439830

Arquivo: visualizadorPyvis.py
Resumo: implementação da ferramenta PyVis para a visualização do grafo
"""


from pathlib import Path
import csv
import json
import math
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
    if "|" not in nome:
        return ""
    return nome.split("|", 1)[1].strip()


def extrair_estacao(nome):
    return nome.split("|", 1)[0].strip()


def carregar_posicoes(grafo, arquivo=None):
    """Converte as coordenadas para uma projeção local, com o norte para cima."""
    if arquivo is None:
        arquivo = Path(__file__).resolve().parent.parent / "dados" / "coordenadas_estacoes.csv"
    if not Path(arquivo).exists() or grafo.n == 0:
        return {}

    coordenadas = {}
    with open(arquivo, encoding="utf-8", newline="") as tabela:
        for registro in csv.DictReader(tabela):
            latitude = float(registro["latitude"])
            longitude = float(registro["longitude"])
            if not math.isfinite(latitude) or not math.isfinite(longitude):
                raise ValueError("As coordenadas devem ser finitas.")
            if not -90 <= latitude <= 90 or not -180 <= longitude <= 180:
                raise ValueError("Coordenadas fora dos limites geográficos.")
            rotulo = registro["rotulo"]
            if rotulo in coordenadas:
                raise ValueError(f"Coordenadas duplicadas para {rotulo}.")
            coordenadas[rotulo] = (latitude, longitude)
    if any(nome not in coordenadas for nome in grafo.rotulos):
        return {}

    pontos = [coordenadas[nome] for nome in grafo.rotulos]
    latitude_media = sum(lat for lat, lon in pontos) / grafo.n
    longitude_media = sum(lon for lat, lon in pontos) / grafo.n
    # Projeção equiretangular local; 20 unidades visuais por quilômetro.
    escala = 6371 * 80
    posicoes = {}
    for indice, (latitude, longitude) in enumerate(pontos):
        posicoes[indice] = {
            "x": escala * math.radians(longitude - longitude_media) * math.cos(math.radians(latitude_media)),
            "y": -escala * math.radians(latitude - latitude_media),
        }
    return posicoes


def criar_controles(grafo):
    """Monta o HTML dos controles e o JavaScript das interações."""
    posicoes = carregar_posicoes(grafo)
    desativado = "" if posicoes else "disabled"
    aviso = "" if posicoes else " O modo geográfico exige coordenadas para todos os vértices."
    vertices = sorted(
        ((grafo.nome_vertice(i), i) for i in range(grafo.n)),
        key=lambda item: (item[0].casefold(), item[1]),
    )
    opcoes = "\n".join(
        f'<option value="{indice}" title="{escape(nome, quote=True)}">{escape(nome)}</option>'
        for nome, indice in vertices
    )
    linhas = {extrair_linha(nome) for nome in grafo.rotulos}
    legenda = "".join(
        f'<span class="linha-legenda"><i style="background:{cor}"></i>{escape(linha.removeprefix("Linha "))}</span>'
        for linha, cor in CORES_LINHAS.items() if linha in linhas
    )
    estilos = """
    <style>
      :root { color-scheme: dark; }
      * { box-sizing: border-box; scrollbar-color: #405060 #101820; scrollbar-width: thin; }
      body { margin: 0; background: #0c1117; color: #e8edf3; font: 14px/1.5 system-ui, sans-serif; }
      body > center, .mapa-conteudo > center { display: none; }
      .app-shell { max-width: 1680px; margin: auto; padding: 28px; }
      .app-header { display: flex; align-items: center; justify-content: space-between; gap: 24px; margin-bottom: 24px; }
      .app-marca { color: #6bcfc1; font-size: 11px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; }
      .app-header h1 { margin: 5px 0; font-size: 28px; font-weight: 650; letter-spacing: -.6px; }
      .app-header p { margin: 0; color: #91a1b3; }
      .rede-resumo { display: flex; gap: 12px; }
      .rede-metrica { min-width: 112px; padding: 12px 18px; border: 1px solid #293440; border-radius: 10px; background: #131b24; }
      .rede-metrica strong { display: block; font-size: 23px; font-weight: 650; line-height: 1.2; }
      .rede-metrica span { color: #91a1b3; font-size: 11px; }
      .rede-workspace { display: grid; grid-template-columns: 340px minmax(0, 1fr); gap: 20px; align-items: start; }
      .painel-controles, .painel-mapa { background: #131b24; border: 1px solid #293440; border-radius: 12px; overflow: hidden; min-width: 0; }
      .painel-bloco { padding: 20px; }
      .painel-bloco + .painel-bloco { border-top: 1px solid #293440; }
      .painel-bloco h2 { margin: 0 0 6px; font-size: 15px; font-weight: 650; }
      .painel-bloco p, .ajuda { margin: 0 0 14px; color: #91a1b3; font-size: 12px; }
      .passo { display: inline-flex; align-items: center; justify-content: center; width: 22px; height: 22px; margin-right: 8px; border-radius: 6px; background: #22303c; color: #b9c9d8; font-size: 11px; }
      .campo-label { display: block; margin-bottom: 8px; font-size: 12px; color: #bfccd8; }
      #seletor-estacao { display: block; width: 100%; height: 224px; padding: 5px; border: 1px solid #354352; border-radius: 8px; background: #0c131b; color: #dbe5ee; font: 12px/1.5 system-ui, sans-serif; }
      #seletor-estacao option { padding: 7px 8px; border-radius: 4px; }
      #seletor-estacao option:checked { background: #256e67 linear-gradient(#256e67, #256e67); color: white; }
      #seletor-estacao option:disabled { color: #62717e; text-decoration: line-through; }
      .botao { display: block; width: 100%; min-height: 42px; padding: 10px 14px; border: 1px solid #354352; border-radius: 8px; background: #1c2834; color: #e8edf3; font: 600 12px system-ui, sans-serif; cursor: pointer; transition: background .15s, border-color .15s; }
      .botao:hover { background: #263746; border-color: #657888; }
      .botao-principal { background: #63d0bb; border-color: #63d0bb; color: #0b2624; }
      .botao-principal:hover { background: #8be0cf; border-color: #8be0cf; }
      .botao-remover { color: #f1b9b8; background: #2b2028; border-color: #65404a; }
      .botao-remover:hover { background: #432a32; border-color: #ab6976; }
      .botoes-simulacao { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
      .botao:focus-visible, #seletor-estacao:focus-visible { outline: 2px solid #8be0cf; outline-offset: 3px; }
      #status-simulacao { margin: 13px 0 0; color: #9cabb9; font-size: 11px; line-height: 1.6; overflow-wrap: anywhere; }
      #resultado-caminho { margin: 14px 0 0; max-height: 240px; overflow: auto; white-space: pre-wrap; overflow-wrap: anywhere; border-left: 2px solid #63d0bb; padding: 12px; background: #0c151c; color: #d9e7e3; font: 12px/1.7 system-ui, sans-serif; }
      #resultado-caminho:empty { display: none; }
      .mapa-cabecalho { display: flex; justify-content: space-between; align-items: center; gap: 12px; flex-wrap: wrap; padding: 16px 20px; border-bottom: 1px solid #293440; }
      .mapa-ferramentas { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
      #modo-layout { min-height: 32px; padding: 5px 8px; border: 1px solid #354352; border-radius: 6px; background: #1c2834; color: #e8edf3; font: 12px system-ui, sans-serif; }
      .mapa-descricao { margin: 0; padding: 10px 20px; color: #91a1b3; font-size: 11px; border-bottom: 1px solid #293440; }
      .mapa-ajustar { width: auto; min-height: 30px; padding: 6px 10px; font-size: 11px; }
      .mapa-cabecalho h2 { margin: 0; font-size: 14px; font-weight: 600; }
      .mapa-cabecalho span { color: #91a1b3; font-size: 11px; }
      .mapa-conteudo { position: relative; }
      .mapa-conteudo .card { width: 100%; border: 0; border-radius: 0; background: transparent; }
      #mynetwork { float: none; width: 100%; height: max(550px, calc(100vh - 245px)) !important; padding: 0; border: 0; background: #101418; }
      #loadingBar { inset: 0; width: 100%; height: 100%; background: #101418e8; }
      #loadingBar .outerBorder { top: 45%; width: min(340px, 85%); height: 48px; border: 1px solid #354352; border-radius: 8px; background: #1c2834; box-shadow: none; }
      #loadingBar #border { left: 12px; top: 20px; width: calc(100% - 72px); height: 8px; border: 0; border-radius: 4px; box-shadow: none; }
      #loadingBar #bar { height: 8px; border: 0; background: #63d0bb; box-shadow: none; }
      #loadingBar #text { left: auto; right: 10px; top: 13px; width: auto; height: auto; color: #dbe5ee; font: 12px system-ui, sans-serif; }
      .rede-legenda { display: flex; flex-wrap: wrap; gap: 9px 16px; padding: 14px 20px; border-top: 1px solid #293440; }
      .linha-legenda { display: inline-flex; align-items: center; gap: 6px; font-size: 10px; color: #a7b6c5; }
      .linha-legenda i { width: 7px; height: 7px; border-radius: 50%; }
      .app-rodape { margin: 15px 0 0; color: #6f8091; font-size: 11px; }
      .vis-navigation .vis-button { filter: grayscale(1) brightness(1.3); }
      .vis-tooltip { max-width: 330px; white-space: pre-line !important; padding: 10px 12px !important; background: #1c2834 !important; color: #e8edf3 !important; border: 1px solid #465567 !important; border-radius: 8px !important; box-shadow: none !important; font: 12px/1.6 system-ui, sans-serif !important; }
      @media (max-width: 900px) {
        .app-shell { padding: 18px; }
        .rede-workspace { grid-template-columns: 290px minmax(0, 1fr); gap: 14px; }
        .painel-bloco { padding: 16px; }
        .mapa-cabecalho span { display: none; }
      }
      @media (max-width: 680px) {
        .app-header { align-items: flex-start; flex-direction: column; gap: 16px; }
        .app-header h1 { font-size: 24px; }
        .rede-resumo { width: 100%; }
        .rede-metrica { flex: 1; }
        .rede-workspace { grid-template-columns: 1fr; }
        #mynetwork { height: 520px !important; }
      }
    </style>
    """
    controles = estilos + f"""
    <div class="app-shell">
      <header class="app-header">
        <div>
          <div class="app-marca">Teoria dos grafos · Análise de redes</div>
          <h1>Rede metroferroviária</h1>
          <p>São Paulo e Região Metropolitana</p>
        </div>
        <div class="rede-resumo" aria-label="Dimensões do grafo original">
          <div class="rede-metrica"><strong>{grafo.n}</strong><span>vértices na rede original</span></div>
          <div class="rede-metrica"><strong>{grafo.m}</strong><span>conexões na rede original</span></div>
        </div>
      </header>
      <div class="rede-workspace">
        <aside class="painel-controles" aria-label="Controles da rede">
          <section class="painel-bloco">
            <h2><span class="passo">01</span>Selecione as estações</h2>
            <p>Use Ctrl ou Command para escolher vários nomes, na lista ou no mapa.</p>
            <label class="campo-label" for="seletor-estacao">Estações e linhas</label>
            <select id="seletor-estacao" multiple size="6">{opcoes}</select>
          </section>
          <section class="painel-bloco">
            <h2><span class="passo">02</span>Encontre um caminho</h2>
            <p>Selecione dois vértices para ver o menor caminho e a distância em quilômetros.</p>
            <button class="botao botao-principal" id="calcular-caminho" type="button">Calcular menor caminho</button>
            <pre id="resultado-caminho" role="status" aria-live="polite"></pre>
          </section>
          <section class="painel-bloco">
            <h2><span class="passo">03</span>Simule uma remoção</h2>
            <p>Remova os selecionados e explore caminhos alternativos na rede.</p>
            <div class="botoes-simulacao">
              <button class="botao botao-remover" id="remover-vertice" type="button">Remover vértices</button>
              <button class="botao" id="restaurar-rede" type="button">Restaurar rede</button>
            </div>
            <p id="status-simulacao" role="status" aria-live="polite">As alterações são temporárias e não modificam o arquivo do grafo.</p>
          </section>
        </aside>
        <main class="painel-mapa" aria-label="Visualização interativa do grafo">
          <div class="mapa-cabecalho">
            <h2>Mapa de conexões</h2>
            <div class="mapa-ferramentas">
              <label for="modo-layout">Disposição</label>
              <select id="modo-layout">
                <option value="livre">Livre</option>
                <option value="geografico" {desativado}>Geográfica</option>
              </select>
              <button class="botao mapa-ajustar" id="ajustar-visao" type="button">Ajustar visão</button>
            </div>
          </div>
          <p class="mapa-descricao" id="descricao-layout" role="status">Livre: distribuição automática por forças.{aviso}</p>
          <div class="mapa-conteudo">
    """
    script = r"""
    <script>
    (function () {
      const seletor = document.getElementById('seletor-estacao');
      const status = document.getElementById('status-simulacao');
      const resultado = document.getElementById('resultado-caminho');
      const nosOriginais = nodes.get();
      const arestasOriginais = edges.get();
      const nomes = new Map(Array.from(seletor.options, opcao => [Number(opcao.value), opcao.textContent]));
      const direcionado = __DIRECIONADO__;
      const modoLayout = document.getElementById('modo-layout');
      const descricaoLayout = document.getElementById('descricao-layout');
      const posicoesGeograficas = __POSICOES__;
      const posicoesLivres = {};

      function aplicarLayout() {
        const geografico = modoLayout.value === 'geografico';
        network.setOptions({physics: {enabled: false}});
        const atualizacoes = nodes.get().map(no => {
          const posicao = geografico ? posicoesGeograficas[no.id] : posicoesLivres[no.id];
          return Object.assign({id: no.id, fixed: geografico, physics: !geografico}, posicao || {});
        });
        nodes.update(atualizacoes);
        network.setOptions({physics: {enabled: !geografico}, interaction: {dragNodes: !geografico}});
        network.redraw();
        network.fit({animation: true});
        descricaoLayout.textContent = geografico
          ? 'Geográfica: coordenadas aproximadas, norte para cima e conexões retas. Estações de integração podem ficar sobrepostas.'
          : 'Livre: distribuição automática por forças.';
      }

      modoLayout.addEventListener('change', function () {
        if (this.value === 'geografico') {
          Object.assign(posicoesLivres, network.getPositions());
        }
        aplicarLayout();
      });

      document.getElementById('ajustar-visao').addEventListener('click', function () {
        network.fit({animation: true});
      });

      function selecionados() {
        return Array.from(seletor.selectedOptions, opcao => Number(opcao.value));
      }

      function limparResultado() {
        resultado.textContent = '';
        network.unselectAll();
      }

      seletor.addEventListener('change', function () {
        const ids = selecionados();
        limparResultado();
        if (ids.length === 0) return;
        network.selectNodes(ids);
        network.fit({nodes: ids, animation: true});
      });

      // Também aceita a seleção diretamente no desenho do grafo.
      network.on('select', function (evento) {
        for (const opcao of seletor.options) {
          opcao.selected = evento.nodes.includes(Number(opcao.value));
        }
        resultado.textContent = '';
      });

      // Dijkstra usa somente os nós e as arestas que ainda estão na visualização.
      function caminhoMinimo(origem, destino) {
        const nosAtuais = nodes.get();
        const vizinhos = new Map(nosAtuais.map(no => [no.id, []]));
        for (const aresta of edges.get()) {
          const peso = Number(aresta.peso);
          if (!Number.isFinite(peso) || peso < 0) {
            throw new Error('O cálculo exige pesos finitos e não negativos.');
          }
          vizinhos.get(aresta.from).push({no: aresta.to, peso: peso, aresta: aresta.id});
          if (!direcionado) {
            vizinhos.get(aresta.to).push({no: aresta.from, peso: peso, aresta: aresta.id});
          }
        }
        const distancias = new Map(nosAtuais.map(no => [no.id, Infinity]));
        const anteriores = new Map();
        const restantes = new Set(distancias.keys());
        distancias.set(origem, 0);
        while (restantes.size > 0) {
          let atual = null;
          for (const id of restantes) {
            if (atual === null || distancias.get(id) < distancias.get(atual)) atual = id;
          }
          if (!Number.isFinite(distancias.get(atual))) break;
          restantes.delete(atual);
          if (atual === destino) break;
          for (const vizinho of vizinhos.get(atual)) {
            const nova = distancias.get(atual) + vizinho.peso;
            if (nova < distancias.get(vizinho.no)) {
              distancias.set(vizinho.no, nova);
              anteriores.set(vizinho.no, {no: atual, aresta: vizinho.aresta});
            }
          }
        }
        if (!Number.isFinite(distancias.get(destino))) return null;
        const caminho = [destino];
        const arestas = [];
        let atual = destino;
        while (atual !== origem) {
          const anterior = anteriores.get(atual);
          arestas.unshift(anterior.aresta);
          atual = anterior.no;
          caminho.unshift(atual);
        }
        return {distancia: distancias.get(destino), caminho: caminho, arestas: arestas};
      }

      document.getElementById('calcular-caminho').addEventListener('click', function () {
        const ids = selecionados();
        if (ids.length !== 2) {
          resultado.textContent = 'Selecione exatamente dois vértices para calcular o caminho.';
          return;
        }
        limparResultado();
        network.selectNodes(ids);
        try {
          const rota = caminhoMinimo(ids[0], ids[1]);
          if (rota === null) {
            resultado.textContent = 'Não existe caminho entre os dois vértices na rede atual.';
            return;
          }
          const distancia = rota.distancia.toFixed(3).replace('.', ',');
          resultado.textContent = 'Distância total aproximada: ' + distancia + ' km\n\n'
            + rota.caminho.map(id => nomes.get(id)).join(' → ');
          network.setSelection({nodes: rota.caminho, edges: rota.arestas}, {highlightEdges: false});
          network.fit({nodes: rota.caminho, animation: true});
        } catch (erro) {
          resultado.textContent = erro.message;
        }
      });

      document.getElementById('remover-vertice').addEventListener('click', function () {
        const ids = selecionados();
        if (ids.length === 0) {
          status.textContent = 'Selecione pelo menos um vértice antes de remover.';
          return;
        }
        for (const id of ids) edges.remove(network.getConnectedEdges(id));
        nodes.remove(ids);
        for (const opcao of seletor.options) {
          if (ids.includes(Number(opcao.value))) opcao.disabled = true;
          opcao.selected = false;
        }
        limparResultado();
        const removidos = nosOriginais.length - nodes.get().length;
        status.textContent = ids.length + ' vértice(s) removido(s). Total removido: ' + removidos + '.';
      });

      document.getElementById('restaurar-rede').addEventListener('click', function () {
        edges.clear();
        nodes.clear();
        nodes.add(nosOriginais);
        edges.add(arestasOriginais);
        for (const opcao of seletor.options) {
          opcao.disabled = false;
          opcao.selected = false;
        }
        limparResultado();
        aplicarLayout();
        status.textContent = 'Rede restaurada. Simulação visual: o arquivo do grafo não será alterado.';
      });
    })();
    </script>
    """.replace('__DIRECIONADO__', 'true' if grafo.direcionado else 'false').replace('__POSICOES__', json.dumps(posicoes))
    fechamento = f"""
          </div>
          <div class="rede-legenda" aria-label="Cores das linhas">{legenda}</div>
        </main>
      </div>
      <p class="app-rodape">Distâncias geográficas aproximadas em km. A disposição geográfica usa coordenadas aproximadas, sem mapa de ruas nem traçado dos trilhos.</p>
    </div>
    """
    return controles, fechamento + script


def adicionar_controles(caminho, grafo):
    """Insere os controles no arquivo HTML gerado pelo PyVis."""
    controles, script = criar_controles(grafo)
    html = caminho.read_text(encoding="utf-8")
    if "<body>" not in html or "</body>" not in html:
        raise ValueError("Não foi possível inserir os controles no HTML gerado pelo PyVis.")
    if '<meta name="viewport"' not in html:
        html = html.replace("<head>", '<head><meta name="viewport" content="width=device-width, initial-scale=1">', 1)
    html = html.replace("<body>", "<body>" + controles, 1)
    html = html.replace("</body>", script + "</body>", 1)
    caminho.write_text(html, encoding="utf-8")


def visualizar_grafo(grafo, arquivo_saida="grafo_completo.html"):
    if grafo is None:
        raise ValueError("Nenhum grafo carregado.")

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

    # Cada nó mantém o ID do grafo, mas exibe o nome da estação.
    for vertice in range(grafo.n):
        nome = grafo.nome_vertice(vertice)
        estacao = extrair_estacao(nome)
        linha = extrair_linha(nome)
        grau = grafo.degree(vertice)
        titulo = (
            f"Estação: {estacao}\n{linha}\n"
            f"Vértice: {vertice}\nGrau: {grau}"
        )
        rede.add_node(
            vertice,
            label=estacao,
            title=titulo,
            size=12 + min(grau * 2, 30),
            color=CORES_LINHAS.get(linha, COR_PADRAO)
        )

    quantidade_arestas = 0
    for origem in range(grafo.n):
        # Em grafos não orientados, desenha cada conexão apenas uma vez.
        inicio = 0 if grafo.direcionado else origem + 1
        for destino in range(inicio, grafo.n):
            if not grafo._tem_aresta(origem, destino):
                continue

            peso = grafo.adj[origem][destino]
            origem_nome = grafo.nome_vertice(origem)
            destino_nome = grafo.nome_vertice(destino)
            if peso == 0:
                titulo = (
                    f"Integração / transferência\n"
                    f"{origem_nome}\n↕\n{destino_nome}"
                )
            else:
                titulo = (
                    f"{origem_nome}\n↔\n{destino_nome}\n"
                    f"Distância: {peso} km"
                )
            rede.add_edge(origem, destino, title=titulo, value=1, peso=float(peso))
            quantidade_arestas += 1

    # Aparência, interação e física ficam configuradas juntas.
    rede.set_options("""
    {
      "nodes": {
        "borderWidth": 2,
        "font": {"size": 13}
      },
      "edges": {
        "smooth": false,
        "font": {"size": 10}
      },
      "interaction": {
        "hover": true,
        "navigationButtons": true,
        "keyboard": true,
        "multiselect": true
      },
      "physics": {
        "enabled": true,
        "solver": "barnesHut",
        "barnesHut": {
          "gravitationalConstant": -10000,
          "centralGravity": 0.15,
          "springLength": 110,
          "springConstant": 0.015,
          "damping": 0.09,
          "avoidOverlap": 0
        },
        "stabilization": {
          "enabled": true,
          "iterations": 1000,
          "updateInterval": 50
        }
      }
    }
    """)

    caminho = Path(arquivo_saida).resolve()
    rede.write_html(str(caminho), open_browser=False)
    adicionar_controles(caminho, grafo)

    print("\n--- Visualização PyVis ---")
    print(f"Vértices: {grafo.n} | Arestas: {quantidade_arestas}")
    print(f"Arquivo: {caminho}")
    webbrowser.open(caminho.as_uri())
    return str(caminho)
