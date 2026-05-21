# Regras De Negócio E Validações

## Autenticação

- o sistema usa um `User` customizado
- login depende de usuário e senha
- usuários precisam estar autenticados para comprar, comentar e anunciar

## Cadastro de PF

Campos principais:

- nome
- sobrenome
- usuário
- e-mail
- senha
- CPF
- data de nascimento
- telefone
- CEP
- endereço

Validações:

- CPF precisa ser real, não só formatado
- senha precisa obedecer às regras do Django
- CPF deve ser único

## Cadastro de PJ

Campos principais:

- usuário
- e-mail
- senha
- CNPJ
- razão social
- nome fantasia
- inscrição estadual
- responsável legal
- CPF do responsável
- telefone
- CEP comercial
- endereço comercial

Validações:

- CNPJ precisa ser real
- CPF do responsável precisa ser real
- CNPJ precisa ser único
- senha precisa obedecer às regras do Django

## Regras de anúncio

- anúncio só pode ser criado por usuário autenticado
- anúncio pertence ao vendedor que o criou
- usuário comum pode vender, trocar ou ambos
- loja só pode vender
- loja só pode anunciar produto novo
- preço precisa ser maior que zero
- anúncio pode ter imagem principal e outras imagens adicionais

## Regras de comentários

- só usuário autenticado pode comentar
- comentário pertence ao anúncio e ao autor
- comentários não devem existir sem anúncio

## Regras de carrinho

- carrinho é único por usuário
- um mesmo anúncio não deve entrar duplicado no carrinho
- carrinho precisa separar futuramente itens de venda e itens de troca

## Regras de loja verificada

- o campo `verified` indica selo de confiança
- o selo deve ser controlado pelo admin
- a loja não deveria poder se autoaprovada

## O que ainda está faltando

- fluxo real de pagamento
- fluxo real de troca com status
- chat persistente para negociação
- validação visual de máscara para CPF/CNPJ
- múltiplas imagens no formulário de criação e edição
- filtros avançados de busca
- bloqueio completo de anúncios fora das regras em todas as entradas possíveis
