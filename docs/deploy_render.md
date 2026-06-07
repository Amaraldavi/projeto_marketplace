# Deploy do Tech Hub no Render (free tier)

Guia passo a passo para publicar o marketplace no [Render](https://render.com).
O projeto já está preparado: `build.sh`, `Procfile`, WhiteNoise, suporte a
`DATABASE_URL` e host/CSRF automáticos via `RENDER_EXTERNAL_HOSTNAME`.

> ⚠️ **Limitações do plano gratuito** (importantes para a apresentação):
> - O **web service** hiberna após ~15 min sem acesso; a 1ª requisição depois disso
>   demora ~30–60s para "acordar" (cold start). Normal, não é erro.
> - O **PostgreSQL gratuito expira ~30 dias** após criado. Anote a data e, se a
>   apresentação for depois disso, recrie o banco antes.
> - O **disco é efêmero**: imagens enviadas por upload (`media/`) **somem a cada
>   deploy/restart**. Para o trabalho acadêmico tudo bem (basta recadastrar alguns
>   anúncios para o demo); para persistir de verdade, use storage externo
>   (Cloudinary/S3) ou um Disk pago.

---

## Pré-requisitos

1. Código no **GitHub** (repositório `Amaraldavi/projeto_marketplace`).
2. Garanta que estes arquivos estão commitados: `requirements.txt`, `build.sh`,
   `Procfile`, `marketplace/settings.py` atualizado. **Nunca** comite a `.env`.
3. Conta no Render (login com o próprio GitHub é o mais simples).

---

## Passo 1 — Criar o banco PostgreSQL

1. No painel do Render: **New +** → **PostgreSQL**.
2. Preencha:
   - **Name**: `techhub-db`
   - **Database** / **User**: pode deixar o padrão
   - **Region**: escolha uma (ex.: **Oregon**) e **use a mesma no web service**.
   - **Plan**: **Free**.
3. **Create Database** e aguarde o status ficar **Available**.
4. Abra o banco e copie a **Internal Database URL** (começa com `postgres://...`).
   Use a *Internal* (mesma região = mais rápido e sem custo de rede).

---

## Passo 2 — Criar o Web Service

1. **New +** → **Web Service** → conecte o repositório do GitHub.
2. Configure:
   - **Name**: `techhub` (a URL será `https://techhub.onrender.com`)
   - **Region**: **a mesma do banco**
   - **Branch**: `main`
   - **Runtime/Language**: **Python 3**
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn marketplace.wsgi:application`
   - **Plan**: **Free**

---

## Passo 3 — Variáveis de ambiente (Environment)

Na aba **Environment** do web service, adicione:

| Key | Value | Observação |
|-----|-------|------------|
| `DATABASE_URL` | *(cole a Internal Database URL do Passo 1)* | conexão com o Postgres |
| `SECRET_KEY` | *(gere uma nova — veja abaixo)* | **não reutilize a local** |
| `DEBUG` | `False` | obrigatório em produção |
| `PYTHON_VERSION` | `3.12.7` | garante wheels das dependências |
| `MERCADO_PAGO_ACCESS_TOKEN` | *(seu token TEST, opcional)* | pagamento é simulado |

Não precisa setar `ALLOWED_HOSTS` nem `CSRF_TRUSTED_ORIGINS`: o `settings.py`
detecta o host do Render automaticamente (`RENDER_EXTERNAL_HOSTNAME`).

**Gerar uma SECRET_KEY nova** (rode local e cole o resultado):

```bash
python -c "from django.core.management.utils import get_random_secret_key as g; print(g())"
```

---

## Passo 4 — Primeiro deploy

1. Clique em **Create Web Service** (ou **Manual Deploy** → **Deploy latest commit**).
2. Acompanhe os **Logs**. O `build.sh` vai:
   - instalar dependências,
   - rodar `collectstatic` (WhiteNoise),
   - rodar `migrate` (cria as tabelas no Postgres).
3. Quando aparecer algo como `Booting worker with pid` e o status ficar **Live**,
   acesse `https://techhub.onrender.com`.

---

## Passo 5 — Criar o usuário admin

O cadastro de superusuário é interativo, então use o **Shell** do Render:

1. No web service, abra a aba **Shell**.
2. Rode:
   ```bash
   python manage.py createsuperuser
   ```
3. Informe usuário, e-mail e uma **senha forte** (não use a senha de teste local).
4. Acesse `https://techhub.onrender.com/admin/` e o **Painel de moderação**.

---

## Passo 6 — Conferência pós-deploy

- [ ] Home abre com CSS aplicado (WhiteNoise servindo estáticos).
- [ ] Login/cadastro funcionam (CSRF ok — sinal de que `CSRF_TRUSTED_ORIGINS` pegou).
- [ ] Criar anúncio, comentar, carrinho e troca funcionam.
- [ ] `/admin/` e `/painel-moderacao/` acessíveis para o admin.
- [ ] `/swagger.html` e `/sobre/` abrem.

---

## Deploys seguintes

Cada `git push` na branch `main` dispara um novo deploy automático (Auto-Deploy
ligado por padrão). O `build.sh` roda `migrate` toda vez, então novas migrações
são aplicadas sozinhas.

---

## Problemas comuns

| Sintoma | Causa provável | Solução |
|---------|----------------|---------|
| `DisallowedHost` | host não reconhecido | confirme que o serviço é Web Service do Render (injeta `RENDER_EXTERNAL_HOSTNAME`); ou adicione o domínio em `ALLOWED_HOSTS` |
| Site sem estilo (CSS quebrado) | `collectstatic` não rodou | verifique o build; confirme `whitenoise` no `requirements.txt` e no MIDDLEWARE |
| `CSRF verification failed` no login | origem não confiável | confira que está acessando via `https://...onrender.com` |
| Erro 500 ao subir | `SECRET_KEY` ausente ou `DEBUG` não setado | confira as variáveis do Passo 3 |
| Build falha em `psycopg2`/`pillow` | versão de Python sem wheel | ajuste `PYTHON_VERSION` (ex.: `3.12.7`) |
| App lento na 1ª visita | cold start do free tier | normal; aguarde ~30–60s |
| Imagens somem após deploy | disco efêmero | esperado no free; recadastre para o demo ou use Cloudinary/S3 |
