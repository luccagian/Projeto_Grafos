# Projeto de Teoria dos Grafos

## Análise da Resiliência da Rede Metroferroviária de São Paulo e Região Metropolitana

Projeto desenvolvido em Python para a disciplina de Teoria dos Grafos da Universidade Presbiteriana Mackenzie.

A aplicação utiliza conceitos de grafos para representar e analisar a rede metroferroviária de São Paulo e Região Metropolitana, considerando estações, linhas, conexões entre estações e pontos de integração.

O foco principal do projeto é a análise estrutural da rede, permitindo verificar conectividade, calcular caminhos mínimos e simular a indisponibilidade de estações.

---

## Integrantes

- Lucas Carmo — 10439830
- Gabriel Medina — 10426931
- Gian Lucca Campanha Ribeiro — 10438361

---

## Organização

O projeto mantém as implementações de grafos e separa as funções de interação em poucas pastas:

- `main.py`: inicia o programa.
- `interface/menu.py`: exibe as opções e encaminha a escolha do usuário.
- `interface/acoes_menu.py`: contém as funções chamadas pelas opções do menu.
- `grafos/grafoMatriz.py` e `grafos/grafoLista.py`: implementações dos grafos.
- `dados/grafo.txt`: dados da rede, com os pesos atualizados em quilômetros.
- `dados/coordenadas_estacoes.csv`: coordenadas para a disposição geográfica no visualizador.
- `visualizacao/visualizadorPyvis.py`: gera a visualização interativa.
- `testes/`: testes dos exercícios e do projeto.
- `executar_testes.py`: executa os testes.

A organização em pastas foi feita para facilitar a manutenção. As funções dos exercícios mantêm nomes como `insereA`, `removeA` e `degree`. As operações comuns usam `remove_vertex`, `show`, `to_file` e `is_connected`; o construtor recebe `tipo_grafo`.

Os arquivos `__init__.py` identificam os pacotes. As pastas `__pycache__` são geradas automaticamente pelo Python e estão incluídas no `.gitignore`.

---

## Executar no Codespaces

No terminal, dentro da pasta que contém `main.py`, execute:

```bash
python -m pip install -r requirements.txt
python main.py
```

Escolha `a` para ler o grafo. As opções `k`, `l` e `m` calculam um caminho mínimo, simulam a falha de uma estação e geram uma visualização interativa. No Codespaces, abra `grafo_completo.html` gerado para visualizar o grafo; a abertura automática de navegador pode não funcionar.

Para executar os testes:

```bash
python executar_testes.py
```

A opção `b` sobrescreve `dados/grafo.txt`. Os pesos são aproximações; Dijkstra exige pesos não negativos. A simulação de falha não altera o grafo carregado.


---

## Modelagem do Grafo

O estudo de caso utiliza um grafo:

- não orientado;
- ponderado nas arestas;
- classificado como tipo 2;
- com 203 vértices;
- com 230 arestas.

Cada vértice representa uma estação associada a uma determinada linha.

Por exemplo:

```text
Sé | Linha 1-Azul
Sé | Linha 3-Vermelha
```

Essas duas ocorrências são representadas por vértices diferentes e conectadas por uma aresta de integração.

As arestas representam:

- conexões entre estações consecutivas da mesma linha;
- integrações entre linhas em uma mesma estação.

O peso das arestas representa uma distância aproximada em quilômetros.

As arestas de integração entre representações da mesma estação possuem peso `0`, pois não representam deslocamento ferroviário entre duas estações diferentes.

---

## Funcionalidades

A aplicação possui um menu interativo com as seguintes opções:

```text
a) Ler dados do arquivo grafo.txt
b) Gravar dados no arquivo grafo.txt
c) Inserir vértice
d) Inserir aresta
e) Remover vértice
f) Remover aresta
g) Mostrar conteúdo do arquivo
h) Mostrar grafo
i) Apresentar conexidade
j) Encerrar a aplicação
k) Calcular caminho mínimo
l) Simular falha de estação
m) Visualizar grafo interativo com PyVis
```

As opções de `a` até `j` correspondem às funcionalidades obrigatórias do projeto.

As opções `k` e `l` foram adicionadas para realizar análises relacionadas ao problema estudado. A opção `m` apresenta a rede em uma visualização interativa.

---

## Visualização com PyVis

A opção `m` gera `grafo_completo.html` a partir do grafo carregado na memória, incluindo alterações feitas pelo menu antes de salvar o TXT. O HTML reúne o desenho da rede, os controles e o cálculo de caminhos no navegador.

### Abrir a visualização

1. Execute `python main.py`.
2. Escolha `a` para carregar `dados/grafo.txt`.
3. Escolha `m` para gerar o HTML.
4. Abra o `grafo_completo.html` gerado. No Codespaces, baixe o arquivo e abra no navegador do computador caso a prévia não o execute corretamente.

Depois de atualizar o código ou o grafo, gere novamente o HTML e atualize a página aberta no navegador.

### Interface e controles

O painel lateral reúne a seleção das estações, o cálculo de caminhos e a simulação de remoções. A área principal mostra o grafo, o seletor de disposição e a legenda das cores das linhas. Os números no cabeçalho descrevem a rede original carregada, antes das remoções visuais.

| Controle | Função |
|---|---|
| Estações e linhas | Seleciona os vértices pelo nome completo, incluindo a linha |
| Calcular menor caminho | Calcula o caminho entre exatamente dois vértices selecionados |
| Remover vértices | Retira temporariamente os selecionados e suas conexões da visualização |
| Restaurar rede | Desfaz todas as remoções visuais e mantém a disposição escolhida |
| Disposição | Alterna entre os modos Livre e Geográfica |
| Ajustar visão | Enquadra os vértices que permanecem na visualização |

Use Ctrl, ou Command no Mac, para selecionar vários nomes na lista ou vários nós no grafo. Passe o mouse sobre uma estação para consultar seu nome, linha e grau; sobre uma aresta, para consultar a distância em quilômetros ou a indicação de integração. Os graus desses avisos se referem ao grafo original.

### Caminho mínimo e remoções

Selecione exatamente dois vértices e clique em **Calcular menor caminho**. O HTML executa Dijkstra com os pesos das arestas, destaca o trajeto e apresenta a distância total aproximada em quilômetros. Caso os vértices estejam desconectados, informa que não existe caminho.

O cálculo usa somente os vértices e as arestas que permanecem na visualização. Após remover vértices, selecione novamente os dois extremos e calcule o caminho para explorar as alternativas disponíveis.

A remoção visual afeta apenas os vértices selecionados, isto é, as combinações de estação e linha. Não remove automaticamente as outras representações da mesma estação. Para analisar a falha de uma estação inteira e suas componentes conexas, use a opção `l` do menu.

As ações do navegador não alteram `dados/grafo.txt` nem o grafo carregado no menu. O botão **Restaurar rede** recupera a rede inicialmente usada para gerar o HTML.

### Disposição livre e geográfica

- **Livre:** usa a simulação de forças do PyVis. Permite arrastar os nós e facilita a exploração das conexões; as posições não são geográficas.
- **Geográfica:** usa latitude e longitude das estações, convertidas em uma projeção local com o norte para cima. A física é desativada e os nós ficam fixos. O zoom e a movimentação da área do mapa continuam disponíveis.

A troca de disposição preserva as remoções, os pesos e os resultados dos caminhos. As conexões geográficas são retas: não há mapa de ruas ao fundo nem reprodução das curvas dos trilhos. Representações de uma mesma estação podem ficar sobrepostas.

Para habilitar a opção geográfica, mantenha estes arquivos na estrutura do projeto:

```text
visualizacao/visualizadorPyvis.py
dados/coordenadas_estacoes.csv
```

O CSV relaciona cada rótulo do grafo à sua latitude e longitude. As informações de código, nome e fonte permitem identificar a origem das coordenadas. O Python inclui as posições no HTML durante a geração; não é necessário consultar o CSV ou acessar a internet para alternar a disposição no HTML já gerado.

Se o CSV estiver ausente ou não contiver coordenadas para todos os rótulos do grafo carregado, a opção geográfica fica desativada, mantendo o modo livre disponível. Caso adicione uma estação ao grafo, inclua também suas coordenadas antes de gerar a visualização geográfica.

### Aparência, escala e manutenção

As cores dos vértices são definidas pela tabela `CORES_LINHAS` em `visualizacao/visualizadorPyvis.py`. As cores são aplicadas diretamente aos nós, sem o parâmetro `group`, para evitar a escolha automática de cores pelo PyVis.

O tamanho dos nós é definido pelo grau, não pela distância ou pelo tamanho real das estações. A projeção geográfica utiliza atualmente 80 unidades visuais por quilômetro:

```python
escala = 6371 * 80
```

O fator `80` pode ser ajustado para mudar a escala das posições em relação ao tamanho dos círculos, mantendo as proporções das coordenadas. Como o enquadramento automático acomoda a rede inteira, use o zoom para explorar regiões com estações próximas. Alterar a escala visual não modifica os pesos nem o cálculo de Dijkstra.

O arquivo do visualizador reúne Python, HTML, CSS e JavaScript. Essa organização mantém a distribuição simples, em um único arquivo. As principais partes são:

- `carregar_posicoes()`: lê as coordenadas e calcula as posições geográficas;
- `criar_controles()`: monta o painel, os estilos e o JavaScript das interações;
- `adicionar_controles()`: insere esse conteúdo no HTML gerado pelo PyVis;
- `visualizar_grafo()`: cria os nós e as arestas, configura o PyVis e gera o arquivo final.

A configuração da física e da interação fica reunida em `set_options()`. Para mudar a apresentação, edite o visualizador e gere novamente o HTML. Evite editar o HTML gerado diretamente, pois a próxima geração substitui esse arquivo.

---

## Matriz de Adjacência

O arquivo `grafos/grafoMatriz.py` contém a principal implementação utilizada pelo projeto.

Entre as funcionalidades disponíveis estão:

- inserção e remoção de vértices;
- inserção e remoção de arestas;
- suporte a grafos dirigidos e não dirigidos;
- suporte a grafos ponderados;
- grau de entrada, saída e grau total;
- identificação de fontes e sorvedouros;
- verificação de simetria;
- verificação de grafo completo;
- cálculo de conexidade;
- identificação de componentes conexas;
- componentes fortemente conexas em grafos dirigidos;
- construção de grafo reduzido;
- leitura do arquivo `grafo.txt`;
- gravação do grafo em arquivo;
- cálculo de caminho mínimo;
- simulação de falha de estação;
- apresentação do grafo em formato de adjacências.

A classe `Grafo` representa grafos dirigidos e a classe `GrafoND` representa grafos não dirigidos.

---

## Lista de Adjacência

O arquivo `grafos/grafoLista.py` contém a implementação baseada em lista de adjacência desenvolvida durante as atividades da disciplina.

Entre as operações disponíveis estão:

- inserção e remoção de arestas;
- grau de entrada, saída e grau total;
- identificação de fontes e sorvedouros;
- comparação entre grafos;
- conversão entre matriz e lista de adjacência;
- inversão das listas de vizinhos;
- verificação de simetria;
- verificação de completude;
- leitura de arquivos;
- remoção de vértices;
- grafos não dirigidos;
- grafo complementar.

A representação principal utilizada no estudo de caso final é a matriz de adjacência.

---

## Caminho Mínimo

A aplicação possui uma funcionalidade para calcular o caminho mínimo entre dois vértices utilizando o algoritmo de Dijkstra.

Como os pesos das arestas representam distâncias aproximadas, o algoritmo determina o caminho com menor distância acumulada entre a origem e o destino.

Todos os pesos utilizados são não negativos, incluindo as integrações de peso `0`, permitindo a utilização do algoritmo de Dijkstra.

Caso os dois vértices estejam em componentes diferentes do grafo, o programa informa que não existe caminho entre eles.

---

## Simulação de Falha de Estação

A opção de simulação de falha permite analisar o comportamento estrutural da rede quando uma determinada estação é considerada indisponível.

Como uma mesma estação pode aparecer em diferentes linhas, todas as ocorrências correspondentes à estação selecionada são temporariamente desconsideradas.

Após isso, o programa recalcula as componentes conexas do grafo restante.

A simulação não altera permanentemente o grafo carregado na memória.

Essa funcionalidade permite observar se a indisponibilidade de uma estação:

- mantém a estrutura restante conectada;
- aumenta a quantidade de componentes;
- separa determinadas regiões da rede.

---

## Requisitos

- Python 3.10 ou superior, para a sintaxe utilizada no código.
- PyVis para gerar a visualização interativa.

Instale as dependências com:

```bash
python -m pip install -r requirements.txt
```

As operações de grafos e os testes utilizam a biblioteca padrão do Python. O PyVis é necessário apenas para a opção `m`. Não é necessário instalar NumPy, PyTorch ou executar os modelos de redes neurais do repositório usado como fonte dos dados.

---

## Como Executar

Abra um terminal na pasta que contém `main.py` e execute:

```bash
python main.py
```

No Windows também pode ser utilizado:

```bash
py main.py
```

Escolha `a` para carregar `dados/grafo.txt`. O arquivo já contém os pesos atualizados em quilômetros; não é necessário recalcular as distâncias a cada execução.

A opção `b` salva o estado atual do grafo sobre `dados/grafo.txt`. A simulação de falha não modifica o grafo carregado.

---

## Executando os Testes

Para executar todos os testes automatizados:

```bash
python executar_testes.py
```

No Windows:

```bash
py executar_testes.py
```

O resultado esperado é:

```text
Ran 42 tests

OK
```

Atualmente a versão distribuída possui 42 testes automatizados.

Eles incluem 30 testes das atividades anteriores da disciplina e 12 testes das adaptações realizadas para o projeto.

---

## Testes Específicos do Projeto

Os testes adicionais verificam, entre outras situações:

- simetria de arestas em grafos não dirigidos;
- remoção de arestas;
- inserção de vértices com rótulos;
- remoção de vértices e suas arestas;
- conexidade de grafos não dirigidos;
- leitura e gravação no formato utilizado pelo projeto;
- prevenção de duplicação de arestas não dirigidas;
- tratamento de grafos dirigidos;
- funcionamento do algoritmo de Dijkstra;
- utilização de arestas de peso zero;
- simulação de falha sem modificar permanentemente o grafo;
- remoção lógica de todas as ocorrências de uma mesma estação durante uma simulação.

---

## Estrutura do Projeto

```text
Projeto_Grafos/
├── main.py
├── executar_testes.py
├── requirements.txt
├── .gitignore
├── README.md
├── interface/
│   ├── __init__.py
│   ├── menu.py
│   └── acoes_menu.py
├── grafos/
│   ├── __init__.py
│   ├── grafoMatriz.py
│   └── grafoLista.py
├── dados/
│   ├── grafo.txt
│   └── coordenadas_estacoes.csv
├── visualizacao/
│   ├── __init__.py
│   └── visualizadorPyvis.py
└── testes/
    ├── __init__.py
    ├── testeExercicios.py
    └── testeProjeto.py
```

O arquivo `dados/grafo.txt` já contém os pesos atualizados. A substituição desse arquivo foi suficiente para o menu, o Dijkstra e o visualizador passarem a usar os novos valores. O cálculo das distâncias foi realizado previamente, fora da execução normal do programa.

---

## Formato do Arquivo `grafo.txt`

O arquivo utilizado pelo projeto segue a seguinte estrutura:

```text
tipo_do_grafo
quantidade_de_vertices
id "rotulo"
id "rotulo"
...
quantidade_de_arestas
vertice_origem vertice_destino peso
vertice_origem vertice_destino peso
...
```

O início do arquivo utilizado no estudo de caso possui estrutura semelhante a:

```text
2
203
0 "Jabaquara-Comitê Paralímpico Brasileiro | Linha 1-Azul"
1 "Conceição | Linha 1-Azul"
2 "São Judas | Linha 1-Azul"
...
230
0 1 1.266387
1 2 1.050555
...
```

Onde:

- `2` representa um grafo não orientado com peso nas arestas;
- `203` representa a quantidade de vértices;
- cada vértice possui um identificador e um rótulo;
- `230` representa a quantidade de arestas;
- cada aresta contém os identificadores de seus vértices e o peso correspondente.

---

## Pesos das Arestas

Os pesos representam distâncias geográficas aproximadas em quilômetros. A base dos dados e do método de cálculo é o repositório [The-Use-of-Graph-Neural-Networks-in-Rail-Transport-Planning](https://github.com/rafaelapz/The-Use-of-Graph-Neural-Networks-in-Rail-Transport-Planning), desenvolvido para o trabalho *The Use of Graph Neural Networks in Rail Transport Planning: A Case Study in the São Paulo Metropolitan Region*, de R. Zyngier e I. Oliveira.

Foram utilizados:

- [`scripts/dados/estacoes.csv`](https://github.com/rafaelapz/The-Use-of-Graph-Neural-Networks-in-Rail-Transport-Planning/blob/main/scripts/dados/estacoes.csv), como fonte das coordenadas das estações;
- [`scripts/distancia_min_e_max.py`](https://github.com/rafaelapz/The-Use-of-Graph-Neural-Networks-in-Rail-Transport-Planning/blob/main/scripts/distancia_min_e_max.py), como referência para o cálculo de Haversine, com raio terrestre de 6371 km.

Os pesos foram calculados previamente a partir dessas coordenadas e incorporados ao arquivo `dados/grafo.txt`. A tabela de tempos de viagem do repositório não foi utilizada, pois o peso adotado neste projeto é distância, em quilômetros.

### Como os pesos foram atualizados

1. Cada rótulo do grafo foi associado à estação correspondente na fonte.
2. As coordenadas foram associadas aos rótulos para o cálculo realizado previamente.
3. Para cada conexão existente entre estações diferentes, foi calculada a distância de Haversine, arredondada para seis casas decimais.
4. As integrações entre representações da mesma estação permaneceram com peso `0`.
5. Os valores foram gravados em `dados/grafo.txt`, mantendo os 203 vértices e as 230 arestas.

Foram atualizados os pesos de 190 trechos, mantendo as 40 integrações com peso zero. As estimativas anteriores baseadas em médias por linha foram substituídas pelo cálculo geográfico.

As diferenças de nome entre as bases foram tratadas explicitamente. Por exemplo, Jabaquara-Comitê Paralímpico Brasileiro corresponde a Terminal Intermodal Jabaquara, e Engenheiro Cardoso corresponde a Eng. Cardoso. Os nomes do nosso grafo foram preservados.

### Uso dos novos pesos

Os novos pesos foram incorporados pela substituição de `dados/grafo.txt`, sem adicionar módulos de recálculo ou arquivos de auditoria. A tabela `dados/coordenadas_estacoes.csv` foi incluída depois para permitir a disposição geográfica opcional no visualizador; sua leitura não altera os pesos do grafo.

O programa lê diretamente os pesos já presentes no TXT. Para utilizá-los, execute `python main.py` e escolha `a` para carregar o grafo. As opções de caminho mínimo e visualização usarão os valores atualizados.

As distâncias não são recalculadas automaticamente durante a execução. Para uma futura alteração, será necessário editar os pesos do TXT ou gerar externamente uma nova versão do arquivo.

### Complemento dos dados e limitações

A base recebida não continha Ambuitá. Por isso, 202 registros de vértices foram associados às coordenadas do repositório e um registro utilizou a coordenada complementar de [Ambuitá no Mapcarta, baseada no OpenStreetMap](https://mapcarta.com/pt/N13724871811): latitude `-23.53024` e longitude `-46.97277`. Essa é a única complementação de coordenadas em relação ao repositório usado como base.

Os resultados dependem da qualidade das coordenadas. Na base utilizada, Lapa possui uma única coordenada, reutilizada nas representações das linhas 7 e 8. As coordenadas de Capuava e Mauá produzem aproximadamente 8,28 km entre elas; esse trecho merece conferência na fonte e foi mantido sem correção automática.

A distância de Haversine não acompanha as curvas dos trilhos. Portanto, os pesos não representam medições exatas de percurso ferroviário nem tempo de viagem. Da mesma forma, integração de peso `0` é uma convenção da modelagem e não significa que a transferência seja instantânea.

---

## Conexidade

A aplicação permite verificar a conexidade do grafo.

Para grafos não dirigidos, o programa informa se a estrutura é conexa ou desconexa e permite analisar suas componentes.

No estudo de caso atual, o grafo é classificado como conexo, ou seja, existe caminho entre quaisquer dois vértices da rede modelada.

---

## Organização das Classes

| Classe | Arquivo | Representação | Tipo |
|---|---|---|---|
| `Grafo` | `grafos/grafoMatriz.py` | Matriz | Dirigido |
| `GrafoND` | `grafos/grafoMatriz.py` | Matriz | Não dirigido |
| `Grafo` | `grafos/grafoLista.py` | Lista | Dirigido |
| `GrafoND` | `grafos/grafoLista.py` | Lista | Não dirigido |

---

## Objetivo do Projeto

O objetivo do projeto é utilizar conceitos e algoritmos de Teoria dos Grafos para representar e analisar estruturalmente a rede metroferroviária de São Paulo e Região Metropolitana.

A análise busca estudar principalmente:

- conectividade da rede;
- caminhos entre diferentes pontos;
- caminhos mínimos;
- efeitos estruturais provocados pela indisponibilidade de estações;
- formação de componentes conexas após falhas.

O projeto possui foco estrutural e não utiliza dados detalhados de demanda ou fluxo de passageiros.
