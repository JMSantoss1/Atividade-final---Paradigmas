# Sistema de Gerenciamento de Biblioteca

Atividade Prática — Linguagens de Programação (Orientação a Objetos e Programação Funcional).

Implementação em **Python 3.9+**, sem dependências externas e sem banco de dados (dados em memória).

Equipe: José Mateus dos Santos e Luiz Henrique da Silva Ramos

## Como executar

```bash
python main.py
python testes.py
```

`main.py` demonstra todas as funcionalidades com datas fixas, para que a saída seja sempre a mesma. `testes.py` executa 11 testes automatizados (`unittest`).

## Estrutura

| Arquivo | Responsabilidade |
|---|---|
| `livro.py` | Classe `Livro` (identificador, título, autor, categoria) |
| `usuario.py` | Classe `Usuario` (identificador, nome, matrícula) |
| `emprestimo.py` | Classe `Emprestimo` (livro, usuário, datas de empréstimo, prevista e efetiva de devolução) |
| `biblioteca.py` | Classe `Biblioteca`: cadastros, consultas, empréstimos, devoluções e acesso a relatórios/estatísticas |
| `funcoes_puras.py` | Núcleo funcional: filtragem, multas, atrasos, relatório e estatísticas |
| `comparacao_paradigmas.py` | Mesma funcionalidade em versão imperativa e funcional |
| `main.py` | Demonstração executável |
| `testes.py` | Testes automatizados |

## Modelagem orientada a objetos

**Relacionamentos**
- `Emprestimo` referencia exatamente um `Livro` e um `Usuario` (multiplicidade `*` para `1` nos dois lados).
- `Biblioteca` agrega `Livro`, `Usuario` e `Emprestimo` (1 para `*`).
- Um `Usuario` pode ter vários `Emprestimo`; um `Livro` pode aparecer em vários `Emprestimo` ao longo do tempo, mas em apenas um ativo por vez.

**Encapsulamento**
- Todos os atributos são privados (prefixo `__`) e expostos somente por propriedades de leitura.
- `Livro`, `Usuario` e `Emprestimo` não possuem setters. Os dados internos da `Biblioteca` (dicionários) nunca são expostos: as consultas devolvem **tuplas**, isto é, cópias imutáveis.
- Os identificadores são gerados internamente pela `Biblioteca`.

**Responsabilidades**
- `Livro` e `Usuario`: representar e validar seus próprios dados.
- `Emprestimo`: representar a retirada, informar se está ativo (`ativo`) e produzir sua versão devolvida (`devolvido_em`).
- `Biblioteca`: aplicar as regras que dependem do estado do sistema (disponibilidade do livro, matrícula única, devolução já registrada) e delegar os cálculos às funções puras.

## Regras de negócio

| Regra | Onde é aplicada |
|---|---|
| 1. Usuário com vários empréstimos; cada empréstimo com um usuário e um livro | `Emprestimo` e `Biblioteca.registrar_emprestimo` |
| 2. Livro não emprestado a mais de um usuário ao mesmo tempo | `Biblioteca.livro_disponivel` e `registrar_emprestimo` (lança `LivroIndisponivel`) |
| 3. Exemplar único | Cada `Livro` é uma unidade; não há controle de cópias |
| 4. Devolução registra a data e libera o livro | `Biblioteca.registrar_devolucao` |
| 5. Atrasado = prazo ultrapassado e não devolvido | `funcoes_puras.calcular_dias_atraso` e `esta_ativo_e_atrasado` |
| 6. Multa de R$ 2,00 por dia | `funcoes_puras.MULTA_DIARIA` e `calcular_multa` |
| 7. Relatório só com ativos e atrasados, com data de referência | `funcoes_puras.gerar_relatorio_multas` |
| 8. Sem reservas, múltiplas cópias ou multa de devolvidos | Não implementado, conforme o enunciado |

Um empréstimo só é considerado atrasado **depois** da data prevista: na própria data prevista ainda não há atraso.

Os valores monetários usam `Decimal`, o que evita erros de arredondamento de ponto flutuante.

## Programação funcional

| Item | Função | Técnica |
|---|---|---|
| 5.1 Filtragem de livros | `filtrar_livros_por_categoria` | `filter`; devolve nova tupla; ignora maiúsculas/minúsculas |
| 5.2 Cálculo de multas | `calcular_multa(dias_atraso, valor_diario)` | Função pura |
| 5.3 Empréstimos atrasados | `selecionar_emprestimos_atrasados` | `filter` |
| 5.4 Relatório de multas | `gerar_relatorio_multas` | `filter` (atrasados), `map` (multa de cada um) e `reduce` (soma) |
| 5.5 Estatísticas | `calcular_estatisticas` | `reduce` em livros por categoria e empréstimos por usuário; `filter` nas contagens de ativos e atrasados |

Funções puras implementadas (mais de três): `filtrar_livros_por_categoria`, `calcular_multa`, `calcular_dias_atraso`, `esta_ativo_e_atrasado`, `selecionar_emprestimos_atrasados`, `criar_item_multa`, `gerar_relatorio_multas`, `contar_livros_por_categoria`, `contar_emprestimos_por_usuario`, `contar_emprestimos_ativos`, `calcular_estatisticas`.

### Imutabilidade e transparência referencial
- Nenhuma função pura altera suas entradas: o resultado é sempre uma nova estrutura (`tuple`, `NamedTuple` ou `MappingProxyType` somente leitura).
- Os `reduce` de contagem não alteram o acumulador. Cada passo cria um novo dicionário com `{**acumulado, chave: novo_valor}`.
- A data de referência sempre chega por parâmetro. Nenhuma função pura lê o relógio do sistema, por isso entradas iguais produzem saídas iguais.
- Devolver um livro não altera o `Emprestimo`: `devolvido_em` cria um novo objeto, que a `Biblioteca` guarda no lugar do anterior.

### Separação entre regras puras e efeitos colaterais
- **Com efeito colateral (altera estado):** `cadastrar_livro`, `cadastrar_usuario`, `registrar_emprestimo` e `registrar_devolucao`, todos em `Biblioteca`.
- **Puro:** todo o módulo `funcoes_puras.py`. Os métodos de relatório e estatística da `Biblioteca` apenas passam um retrato imutável do estado (`tuple`) para essas funções.
- `main.py` concentra a saída no console (`print`).

## Comparação entre paradigmas

Funcionalidade escolhida: **valor total das multas** (`comparacao_paradigmas.py`).

- `total_multas_imperativo`: laço `for`, condicionais aninhadas e acumulador `total` reatribuído a cada volta.
- `total_multas_funcional`: `filter` seleciona os atrasados, `map` calcula cada multa e `reduce` soma.
- `comparar_paradigmas` executa as duas versões e confirma que o resultado é o mesmo.

A versão imperativa mistura seleção, cálculo e acumulação no mesmo bloco, e a variável `total` muda ao longo da execução. A funcional separa cada etapa em uma operação nomeada, sem variáveis mutáveis, o que facilita testar e reaproveitar as partes.

## Exemplo de saída (`main.py`, data de referência 10/11/2026)

```
RELATÓRIO DE MULTAS EM 10/11/2026
  #1 Clean Code | Ana Souza | 33 dia(s) | R$ 66,00
  #2 Python Fluente | Bruno Lima | 17 dia(s) | R$ 34,00
  #3 Structure and Interpretation of Computer Programs | Ana Souza | 7 dia(s) | R$ 14,00
  #4 Introdução a Algoritmos | Carla Dias | 2 dia(s) | R$ 4,00
  TOTAL: R$ 118,00
```

O empréstimo #5 foi devolvido, então não entra no relatório.

## Observação sobre o código

Conforme o enunciado, o código-fonte não contém comentários. A documentação está neste README e a clareza vem dos nomes de classes, funções e variáveis.
