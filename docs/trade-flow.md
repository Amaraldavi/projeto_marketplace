# Fluxo De Troca

## Objetivo

Separar claramente a troca da compra.

- compra segue para pagamento
- troca segue para negociação
- a negociação pode envolver uma ou mais mensagens
- o status da troca precisa indicar o andamento sem confundir o usuário

## Modelo sugerido

### `TradeRequest`
Representa uma solicitação de troca entre duas partes.

Campos principais:

- `requester`: quem iniciou a troca
- `counterparty`: vendedor do anúncio
- `listing`: anúncio principal da negociação
- `status`: estado da solicitação
- `initial_message`: mensagem inicial da proposta
- `created_at`
- `updated_at`

### `TradeMessage`
Representa as mensagens da negociação.

Campos principais:

- `trade_request`
- `sender`
- `content`
- `created_at`

## Status recomendados

- `pending`: aguardando análise ou primeira resposta
- `negotiating`: em conversa ativa
- `approved`: proposta aceita
- `rejected`: proposta recusada
- `completed`: troca concluída
- `cancelled`: negociação cancelada

## Fluxo recomendado para o usuário

1. usuário adiciona itens ao carrinho
2. sistema separa o que é venda e o que é troca
3. itens de venda seguem para pagamento
4. itens de troca criam uma `TradeRequest`
5. o sistema abre uma conversa entre as partes
6. vendedor aprova, recusa ou pede ajuste
7. se aprovado, a troca pode avançar para conclusão

## Como lidar com vários itens e vários donos

O caminho mais simples é separar por vendedor.

Exemplo:

- carrinho com 3 itens de 2 vendedores diferentes
- o sistema cria 2 solicitações de troca, uma por vendedor
- cada solicitação mantém sua própria conversa e status

Isso evita misturar interlocutores e deixa a negociação mais clara.

## O que ainda falta implementar na interface

- tela para listar negociações de troca
- tela para responder mensagens da troca
- botão para aprovar ou reprovar a troca
- integração do carrinho com a criação das solicitações
