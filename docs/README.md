# Guia do Projeto Marketplace

Este diretório organiza o projeto em uma leitura mais simples do que existe hoje, o que já funciona e o que ainda precisa ser evoluído.

## Objetivo do sistema

Marketplace para produtos eletrônicos com dois perfis principais:

- Pessoa física: pode comprar, vender e propor troca.
- Loja/PJ: pode vender, ter selo de verificação e anunciar apenas produtos novos.

## Arquivos do guia

- [Entidades e relacionamentos](entidades.md)
- [Fluxos do sistema](fluxos.md)
- [Regras de negócio e validações](regras-negocio.md)
- [Fluxo de troca](trade-flow.md)
- [Pagamento e entrega](payment-delivery.md)
- [Mapa de endpoints](endpoints.md)
- [Roadmap de evolução](roadmap.md)

## Leitura recomendada

1. Comece por `entidades.md` para entender as tabelas.
2. Depois leia `fluxos.md` para ver como login, anúncio, carrinho e troca funcionam.
3. Em seguida, use `regras-negocio.md` para enxergar o que já está validado.
4. Por fim, siga `roadmap.md` para decidir o que implementar primeiro.

## Estado atual resumido

- Autenticação customizada já existe com `User` próprio.
- Cadastro PF/PJ já separa perfis.
- Home exibe anúncios, destaques e busca simples.
- Carrinho existe para itens de compra.
- Comentários existem no detalhe do anúncio.
- Troca ainda precisa virar um fluxo próprio, separado da compra.
