# Projeto Marketplace

## 👥 1. Definição de Usuários e Regras de Negócio

### Usuário Comum (Pessoa Física)
* Pode comprar produtos de lojas ou de outros usuários.
* Pode criar anúncios do tipo **Venda** ou **Troca** (ex: produtos usados ou seminovos).

### Loja (Pessoa Jurídica - CNPJ)
* Pode vender produtos (geralmente novos).
* Pode criar anúncios apenas do tipo **Venda** (não participam de trocas).
* Terá um indicativo visual de "Loja Verificada" para gerar mais confiança na plataforma.

---

## ⚙️ 2. Requisitos Funcionais (RF)

* **RF01:** Permitir o cadastro de usuários comuns (com CPF) e lojas (com CNPJ), validando a unicidade dos documentos.
* **RF02:** Permitir a criação de anúncios contendo título, descrição, categoria, preço, condição (Novo/Usado) e upload de múltiplas imagens.
* **RF03:** Restringir o tipo de anúncio com base no perfil (Lojas: apenas "Venda"; Usuários Comuns: "Venda" ou "Troca").
* **RF04:** Disponibilizar campo de busca e filtros avançados (por hardware específico, estado de conservação, faixa de preço e tipo de vendedor).
* **RF05:** Possuir um chat (Assíncrono) interno para comunicação direta entre o comprador e o vendedor.
* **RF06:** Permitir que compradores avaliem o vendedor ou loja após a conclusão da negociação.

---

## 🚀 3. Requisitos Não Funcionais (RNF)

* **RNF01 (Tecnologia):** O backend será desenvolvido em Python com o framework Django.
* **RNF02 (Banco de Dados):** Utilização de um banco de dados relacional robusto (SQL Server ou PostgreSQL).
* **RNF03 (Comunicação):** Sistema de mensagens rápido e responsivo (via chamadas assíncronas com JavaScript ou WebSockets usando Django Channels).
* **RNF04 (Armazenamento):** As imagens dos anúncios devem ser salvas em um serviço de cloud storage (AWS S3, Cloudinary).
* **RNF05 (Responsividade):** A interface deve funcionar perfeitamente em dispositivos móveis e desktops.

---

## 📂 4. Organização do Projeto no Django (Apps)

* `accounts`: Lida com o modelo customizado de usuário (`AbstractUser`), login, registro, recuperação de senha e perfis (Loja vs Comum).
* `marketplace`: Contém os modelos de Categorias, Produtos/Anúncios, Imagens dos Produtos e Avaliações.
* `chat`: Dedicado à troca de mensagens, contendo os modelos de `Thread` (conversa) e `Message` (conteúdo).
* `core`: App genérico para páginas estáticas (Home, Termos de Uso, Sobre nós e template base).

---

## 🗄️ 5. Esboço de Modelagem de Dados

* `User`: Modelo base herdando do Django, com um campo booleano `is_store`.
* `StoreProfile` / `CommonProfile`: Relação *One-to-One* com o usuário (CNPJ e Razão Social para lojas; CPF para usuários comuns).
* `Category`: Nome e slug (ex: Placas de Vídeo, `placas-de-video`).
* `Listing` (Anúncio): Chave estrangeira (FK) para o Vendedor e Categoria. Campos de texto, preço, tipo (Venda/Troca) e status (Ativo, Pausado, Vendido).
* `ListingImage`: Chave estrangeira para o Anúncio e um `ImageField`.
* `Message`: Chave estrangeira para o Remetente, Destinatário e Anúncio, além do texto e *timestamp*.
