# Pagamento E Entrega

## Como pagamento deve funcionar

Para um marketplace, o caminho mais seguro e mais comum não é redirecionar o usuário direto para o banco dele em qualquer situação.

O fluxo mais inteligente é usar um gateway ou intermediador de pagamento, por exemplo:

- Mercado Pago
- Pagar.me
- Stripe
- PagSeguro
- outro provedor com checkout e split de pagamento

## O que o sistema faz agora

O checkout já está preparado para gerar uma preferência de pagamento em gateway quando houver credenciais configuradas.

No estado atual:

- o pedido é criado no sistema
- a entrega fica registrada no pedido
- o checkout tenta criar uma preferência de pagamento no Mercado Pago
- se o gateway estiver configurado, o usuário é redirecionado para a página de pagamento
- se não estiver configurado, o pedido continua registrado localmente

### O que isso resolve

- o comprador paga dentro de um fluxo controlado
- o marketplace pode confirmar o pagamento sem depender de tela externa do banco
- o vendedor só precisa ter os dados cadastrados quando houver repasse/settlement
- o sistema fica mais simples de testar e manter

## O usuário precisa cadastrar dados bancários?

Depende do modelo de negócio.

### Caso 1: marketplace com gateway e repasse

Nesse caso, normalmente o vendedor/loja cadastra:

- nome do titular
- documento
- banco ou chave PIX
- dados para repasse no painel do provedor

O comprador não precisa cadastrar banco.

### Caso mais prático para este projeto

Para evitar complexidade no início:

- o comprador paga pelo checkout do gateway
- a plataforma controla a confirmação
- o vendedor só cadastra dados de recebimento no provedor, quando isso for necessário

### Caso 2: transferência direta entre as partes

Nesse caso, o sistema teria que guardar os dados bancários de quem recebe e de quem paga, o que é menos seguro e menos prático.

Não recomendo esse modelo para o MVP.

## O que existe no sistema hoje

Hoje o projeto já guarda:

- pedido com método de pagamento escolhido
- método de entrega escolhido
- itens do pedido

Mas ainda não existe integração real com gateway de pagamento.

Ou seja:

- a tela de checkout existe
- o pedido é registrado
- a confirmação de pagamento real ainda é futura

## Como eu recomendo estruturar o pagamento no MVP

### Para compra

- usuário escolhe método de pagamento
- sistema cria o pedido
- integração com gateway vem depois
- status do pedido fica como aguardando pagamento

### Para troca

- não existe pagamento direto
- a troca segue para negociação e aceite
- só depois a troca avança para concluída

## Como a entrega deve funcionar

Hoje não existe integração de entrega automática.

Para o MVP, o mais simples é deixar o sistema trabalhar com três possibilidades:

- retirada presencial
- frete definido pelo vendedor
- a combinar entre as partes

## O que já existe no código

- modelo de entrega por pedido
- endereço do destinatário
- método de entrega
- frete básico
- transportadora
- código de rastreio
- status de entrega
- previsão de entrega
- área administrativa para atualizar esses dados

### O que eu acho mais inteligente agora

No início, eu evitaria integrar transportadora direto.

Motivos:

- aumenta muito a complexidade
- exige cálculo de frete, endereço, etiquetas e rastreio
- atrasa a validação da ideia principal do marketplace

## Recomendação prática

Para a primeira versão, eu faria assim:

- compra: checkout com pagamento registrado e depois integração com gateway
- troca: negociação interna
- entrega: campo de opção no pedido, sem automação de transportadora

Quando a compra estiver estável, aí vale decidir se o sistema vai:

- apenas registrar a entrega combinada
- ou integrar com transportadora e rastreamento
