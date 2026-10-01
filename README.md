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
```

As opções de `a` até `j` correspondem às funcionalidades obrigatórias do projeto.

As opções `k` e `l` foram adicionadas para realizar análises relacionadas ao problema estudado.

---

## Matriz de Adjacência

O arquivo `grafoMatriz.py` contém a principal implementação utilizada pelo projeto.

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

O arquivo `grafoLista.py` contém a implementação baseada em lista de adjacência desenvolvida durante as atividades da disciplina.

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

- Python 3

Não é necessária a instalação de bibliotecas externas para executar a aplicação.

O projeto utiliza apenas módulos da biblioteca padrão do Python.

---

## Como Executar

Abra um terminal na pasta do projeto.

Para iniciar a aplicação:

```bash
python menu.py
```

No Windows também pode ser utilizado:

```bash
py menu.py
```

O programa exibirá o menu principal e permitirá carregar o arquivo `grafo.txt`.

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

Atualmente o projeto possui 42 testes automatizados.

Eles incluem os 30 testes das atividades anteriores da disciplina e 12 testes específicos das adaptações realizadas para o projeto.

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
├── grafoMatriz.py
├── grafoLista.py
├── menu.py
├── grafo.txt
├── testeExercicios.py
├── testeProjeto.py
├── executar_testes.py
└── README.md
```

### Descrição dos arquivos

| Arquivo | Descrição |
|---|---|
| `grafoMatriz.py` | Classes e operações principais sobre grafos utilizando matriz de adjacência |
| `grafoLista.py` | Implementação utilizando lista de adjacência |
| `menu.py` | Menu principal e interação com o usuário |
| `grafo.txt` | Dados do estudo de caso da rede metroferroviária |
| `testeExercicios.py` | Testes das atividades anteriores da disciplina |
| `testeProjeto.py` | Testes específicos das funcionalidades do projeto |
| `executar_testes.py` | Executa todos os testes automatizados |
| `README.md` | Documentação do projeto |

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
0 1 0.917
1 2 0.917
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

Os pesos representam distâncias aproximadas em quilômetros.

Quando havia um valor específico disponível para determinado trecho, esse valor foi utilizado.

Para os demais segmentos foram utilizadas estimativas baseadas nas distâncias médias entre as estações das respectivas linhas.

Por esse motivo, os pesos devem ser interpretados como aproximações utilizadas para a modelagem computacional, e não como medições exatas de todos os trechos ferroviários.

As conexões de integração entre linhas em uma mesma estação utilizam peso `0`.

---

## Conexidade

A aplicação permite verificar a conexidade do grafo.

Para grafos não dirigidos, o programa informa se a estrutura é conexa ou desconexa e permite analisar suas componentes.

No estudo de caso atual, o grafo é classificado como conexo, ou seja, existe caminho entre quaisquer dois vértices da rede modelada.

---

## Organização das Classes

| Classe | Arquivo | Representação | Tipo |
|---|---|---|---|
| `Grafo` | `grafoMatriz.py` | Matriz | Dirigido |
| `GrafoND` | `grafoMatriz.py` | Matriz | Não dirigido |
| `Grafo` | `grafoLista.py` | Lista | Dirigido |
| `GrafoND` | `grafoLista.py` | Lista | Não dirigido |

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
