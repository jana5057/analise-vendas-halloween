# Análise de vendas de Halloween – Festa em Cena

Projeto do Módulo 1 (Machine Learning e Visão Computacional). O programa lê o arquivo `halloween_vendas.csv` (1500 pedidos de 2024 e 2025, em 3 canais: Mercado, Loja física e Web), limpa os dados e gera um relatório de pedidos por canal e por mês. Foi feito em Python, com a biblioteca `csv`, e com Pandas para conferir a leitura.

> Uso de IA: o código foi desenvolvido com ajuda de uma IA, passo a passo, em branches (uma por etapa).

## Colunas principais

| Coluna | O que é | Problema encontrado |
|---|---|---|
| `categoria` | tipo do produto (fantasia ou acessório) | espaços, maiúsculas, pontuação e 18 vazios |
| `canal_venda` | onde o pedido foi feito | escritas diferentes do mesmo canal (45 corrigidos) |
| `data_venda` | data e hora do pedido | 4 datas em formato inválido |
| `data_entrega` | data de entrega | 143 vazias |

## Regras aplicadas

- **Categoria:** tira espaços, deixa minúscula, remove pontuação; se ficar vazia, vira `sem categoria`.
- **Canal:** compara com uma tabela de nomes oficiais (Mercado, Loja física, Web). Se não reconhecer, mantém o texto original e conta à parte.
- **Quantidade e preço:** quantidade precisa ser inteira e maior que zero; preço precisa ser número maior ou igual a zero. Os problemas são só **marcados**, nenhum valor é inventado ou apagado.
- **Datas:** `data_venda` é convertida para data de verdade; as inválidas ficam fora da contagem por mês.
- **Contagens:** entram todos os status (inclusive Cancelado). Contam-se **pedidos registrados**, não receita nem unidades.

## Como rodar

1. Instale o Python 3 e o Pandas: `pip install pandas`
2. Deixe `main.py` e `halloween_vendas.csv` na mesma pasta.
3. No terminal, dentro da pasta, rode: `python main.py`

## Resultados

| Verificação | Resultado |
|---|---|
| Pedidos lidos (csv e Pandas) | 1500 |
| Categorias vazias preenchidas | 18 |
| Categorias não vazias alteradas | 1482 |
| Canais corrigidos / não reconhecidos | 45 / 0 |
| Problemas em quantidade / preço | 7 / 12 |
| Pedidos com algum problema numérico | 19 |
| Datas vazias / inválidas | 0 / 4 |
| Sem data de entrega e Cancelado | 109 |
| Sem data de entrega e outro status | 34 |

**Pedidos por canal:** Web 666, Loja física 551, Mercado 283.

**Pedidos por ano-mês** (4 pedidos com data inválida ficam de fora): 2024-08: 77 · 2024-09: 104 · 2024-10: 393 · 2024-11: 174 · 2025-08: 62 · 2025-09: 94 · 2025-10: 410 · 2025-11: 182

## Duas descobertas

**1. Outubro concentra os pedidos.** Em 2024 e 2025, outubro teve 393 e 410 pedidos, somando 803 dos 1496 pedidos com data válida (cerca de 54%). Interpretação: a procura se concentra no mês do Halloween. Limitação: os dados cobrem só agosto a novembro, contam pedidos (não receita) e 4 pedidos com data inválida ficaram de fora.

**2. Nem todo pedido sem data de entrega é Cancelado.** Dos 143 pedidos sem `data_entrega`, 109 (76%) são Cancelado, mas 34 têm outro status (por exemplo, os pedidos 1170, 990 e 740, todos Concluído). Interpretação: a ausência de data de entrega sozinha não indica cancelamento. Limitação: o arquivo não explica a causa (pode ser falha de registro), e só olhamos exemplos, sem investigar um a um.

## Reflexão: qualidade dos dados e Machine Learning

Um modelo de Machine Learning aprende com os dados que recebe. Se "Web", " web " e "WEB" forem tratados como canais diferentes, o modelo enxerga três canais onde existe um só. Datas inválidas e valores vazios também atrapalham o aprendizado. Além disso, a regra "sem entrega = cancelado" parece lógica, mas está errada em 34 pedidos: se ela fosse usada para criar a resposta que o modelo deve aprender, ele aprenderia um erro. Por isso a limpeza e a validação vêm antes de qualquer modelo, e as decisões (o que foi corrigido, o que ficou de fora) precisam ser registradas, como fizemos aqui.