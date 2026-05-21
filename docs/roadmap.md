# Roadmap De Evolução

## Fase 1 - Organizar a base

- validar CPF e CNPJ de verdade
- manter PF e PJ bem separados
- restringir loja a produto novo
- documentar a estrutura atual
- limpar código duplicado e fluxo confuso

## Fase 2 - Comprar e trocar com clareza

- separar carrinho de compra do fluxo de troca
- criar solicitação de troca
- criar status de negociação
- abrir conversa entre interessados
- registrar aceite, recusa e encerramento
- base inicial da negociação já está sendo criada com `TradeRequest` e `TradeMessage`

## Fase 3 - Pagamento e logística

- escolher provedor de pagamento
- definir repasse para vendedor/loja
- definir se o frete será do sistema, do vendedor ou externo
- integrar confirmação de pagamento
- checkout, pedido e seleção de entrega já estão estruturados na base
- integração inicial com Mercado Pago já está prevista no checkout
- entrega já possui modelo básico com endereço, frete e rastreio

## Fase 4 - Melhorias de produto

- múltiplas imagens no formulário
- filtros mais fortes na busca
- ordenação por preço, relevância e data
- selo de loja verificada controlado pelo admin
- painel administrativo melhor organizado

## Decisão que eu recomendo agora

Para seguir sem travar o projeto, eu faria nesta ordem:

1. fechar validação e regras de cadastro
2. separar compra de troca com status próprio
3. implementar o chat da troca
4. só depois entrar em pagamento e logística

## Observação sobre entrega e transporte

Ainda não é obrigatório o sistema prover transportadora.

Para MVP, o mais simples é:

- a plataforma cuida da negociação e registro
- a logística fica combinada entre as partes
- o frete pode ser definido depois, quando o pagamento estiver estável
