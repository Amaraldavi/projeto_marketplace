# projeto_marketplace

1. Definição de Usuários e Regras de Negócio
Para que o sistema entenda quem pode fazer o quê, precisamos dividir as responsabilidades.

Usuário Comum (Pessoa Física):

Pode comprar produtos de lojas ou de outros usuários.

Pode criar anúncios do tipo Venda ou Troca (ex: produtos usados ou semi-novos).

Loja (Pessoa Jurídica - CNPJ):

Pode vender produtos (geralmente novos).

Pode criar anúncios apenas do tipo Venda. Não participam de trocas.

Terão um selo ou indicativo visual de "Loja Verificada" para gerar mais confiança na plataforma.

2. Requisitos Funcionais (RF)
O que o sistema DEVE fazer.

RF01: O sistema deve permitir o cadastro de usuários comuns (com CPF) e lojas (com CNPJ), validando a unicidade desses documentos.

RF02: O sistema deve permitir a criação de anúncios contendo título, descrição, categoria (Placa de Vídeo, Processador, Periféricos, etc.), preço, condição (Novo/Usado) e upload de múltiplas imagens.

RF03: O sistema deve restringir o tipo de anúncio com base no perfil: Lojas só podem selecionar "Venda"; Usuários Comuns podem selecionar "Venda" ou "Troca".

RF04: O sistema deve ter um campo de busca e filtros avançados (filtrar por hardware específico, estado de conservação, faixa de preço e tipo de vendedor).

RF05: O sistema deve possuir um chat interno para comunicação direta entre o comprador e o vendedor (para negociar peças ou valores).

RF06: O sistema deve permitir que compradores avaliem o vendedor ou loja após a conclusão de uma negociação.

3. Requisitos Não Funcionais (RNF)
Como o sistema deve se comportar tecnicamente.

RNF01 (Tecnologia): O backend será desenvolvido em Python com o framework Django.

RNF02 (Banco de Dados): Utilização de um banco de dados relacional robusto (como SQL Server ou PostgreSQL) para garantir a integridade das transações e relacionamentos.

RNF03 (Comunicação): O sistema de mensagens deve ser rápido e responsivo. Pode ser implementado inicialmente com chamadas assíncronas simples via JavaScript ou evoluído para WebSockets usando Django Channels.

RNF04 (Armazenamento): As imagens dos anúncios devem ser salvas em um serviço de cloud storage (como AWS S3 ou Cloudinary) para não sobrecarregar o servidor local.

RNF05 (Responsividade): A interface deve funcionar perfeitamente em dispositivos móveis e desktops.

4. Organização do Projeto no Django (Apps)
Para manter o código limpo e modular, você pode dividir o projeto em pequenos "Apps" dentro do Django. Sugiro a seguinte estrutura:

accounts: Responsável por toda a parte de usuários. Aqui ficará o seu modelo customizado de usuário (AbstractUser), além das lógicas de login, registro, recuperação de senha e perfis (Loja vs Comum).

marketplace: O coração do negócio. Conterá os modelos de Categorias, Produtos/Anúncios, Imagens dos Produtos e Avaliações.

chat: Um app dedicado apenas para a troca de mensagens, contendo os modelos de Thread (a conversa entre duas pessoas) e Message (o conteúdo da mensagem).

core: Um app genérico para páginas estáticas, como a Home principal, termos de uso, página "Sobre nós" e o template base.

5. Esboço de Modelagem de Dados (Entidades)
Para dar um norte inicial no seu models.py:

User: Modelo base herdando do Django, com um campo booleano is_store para diferenciar rapidamente.

StoreProfile / CommonProfile: Tabelas com relação One-to-One com o usuário, guardando dados específicos (CNPJ e Razão Social para lojas; CPF para usuários comuns).

Category: Nome e slug (ex: Placas de Vídeo, placas-de-video).

Listing (Anúncio): Chave estrangeira para o Usuário (vendedor) e Categoria. Campos de texto, preço, tipo (Venda, Troca) e status (Ativo, Pausado, Vendido).

ListingImage: Chave estrangeira para o Anúncio e um ImageField.

Message: Chave estrangeira para o Remetente, Destinatário, e o Anúncio em questão, além do texto e timestamp.
