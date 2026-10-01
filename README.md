# Projeto de Teoria dos Grafos

Implementação em Python de operações sobre grafos usando matriz de adjacência e lista de adjacência.

O projeto foi desenvolvido como atividade de Teoria dos Grafos e contém exercícios para grafos dirigidos, não dirigidos e ponderados.

## Integrantes:
- Lucas Franco 10439830
- Gabriel Medina 10426931
- Gian Lucca 10438361

## Funcionalidades

### Matriz de adjacência

O arquivo `grafoMatriz.py` implementa:

- inserção e remoção de arestas;
- grau de entrada, grau de saída e grau total;
- identificação de fontes e sorvedouros;
- verificação de simetria e completude;
- grafos não dirigidos com a classe `GrafoND`;
- grafos ponderados com a classe `GrafoPonderado`;
- leitura de grafos a partir de arquivos;
- remoção de vértices;
- grafo complementar;
- tipos de conexidade de grafos dirigidos e não dirigidos;
- grafo reduzido baseado nas componentes fortemente conexas;
- impressão da matriz com o método `show()`.

### Lista de adjacência

O arquivo `grafoLista.py` implementa:

- inserção e remoção de arestas;
- grau de entrada, grau de saída e grau total;
- identificação de fontes e sorvedouros;
- comparação entre grafos;
- conversão entre matriz e lista de adjacência;
- inversão da ordem das listas de vizinhos;
- verificação de simetria e completude;
- leitura de arquivos;
- remoção de vértices;
- grafos não dirigidos com a classe `GrafoND`;
- grafo complementar.

## Requisitos

- Python 3
- Nenhuma biblioteca externa é necessária. O projeto utiliza apenas a biblioteca padrão do Python.

## Como executar

Abra um terminal na pasta do projeto e execute:

```bash
python executar_testes.py
```

No Windows, também é possível usar:

```bash
py executar_testes.py
```

O resultado esperado é semelhante a:

```text
Ran 30 tests

OK
```

Cada teste possui o número do exercício correspondente no nome, de `test_exercicio_01_...` até `test_exercicio_30_...`.

## Estrutura do projeto

```text
Projeto_Grafos-main/
├── grafoMatriz.py       # Implementação com matriz de adjacência
├── grafoLista.py        # Implementação com lista de adjacência
├── testeExercicios.py   # Testes dos 30 exercícios
├── executar_testes.py   # Executor dos testes
├── grafo.txt            # Exemplo de grafo ponderado
└── README.md            # Documentação do projeto
```

## Formato do arquivo de entrada

O arquivo de entrada possui este formato:

```text
V
A
origem destino peso
origem destino peso
...
```

No `grafo.txt` deste projeto:

- `V = 82`: quantidade de vértices;
- `A = 214`: quantidade de registros de arestas;
- cada registro possui origem, destino e peso.

Exemplo:

```text
82
214
0 1 2.5
1 0 2.5
1 2 2.5
```

Quando o arquivo possui três valores por aresta, a leitura pela matriz reconhece o grafo como ponderado. A leitura pela lista utiliza os dois primeiros valores, origem e destino.

## Exemplo de uso

### Grafo com matriz de adjacência

```python
from grafoMatriz import Grafo

grafo = Grafo.from_file("grafo.txt")

print("Vértices:", grafo.n)
print("Arestas:", grafo.m)
print("Grau de entrada do vértice 1:", grafo.inDegree(1))
print("Grau de saída do vértice 1:", grafo.outDegree(1))
```

### Grafo com lista de adjacência

```python
from grafoLista import Grafo

grafo = Grafo.from_file("grafo.txt")

print("Vértices:", grafo.n)
print("Arestas:", grafo.m)
grafo.show()
```

## Testes

Os testes verificam individualmente os 30 exercícios, incluindo:

- graus de entrada e saída;
- fontes e sorvedouros;
- simetria e completude;
- leitura de arquivos;
- grafos ponderados;
- inserção, remoção de arestas e remoção de vértices;
- complemento e conexidade;
- grafo reduzido;
- conversão entre representações;
- igualdade e inversão de listas;
- saída do método `show()`.

## Organização das classes

| Classe | Representação | Tipo de grafo |
|---|---|---|
| `Grafo` em `grafoMatriz.py` | Matriz | Dirigido |
| `GrafoND` em `grafoMatriz.py` | Matriz | Não dirigido |
| `GrafoPonderado` em `grafoMatriz.py` | Matriz | Dirigido ponderado |
| `Grafo` em `grafoLista.py` | Lista | Dirigido |
| `GrafoND` em `grafoLista.py` | Lista | Não dirigido |
