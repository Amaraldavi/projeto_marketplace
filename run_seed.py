"""
Executa o seed_render.sql no banco PostgreSQL da Render (ou qualquer outro).

Uso (PowerShell, dentro da pasta do projeto):

    # 1) cole a External Database URL da Render numa variavel de ambiente
    $env:DATABASE_URL = "postgresql://usuario:senha@dpg-xxxx.render.com/nome_banco"

    # 2) rode com o Python da venv
    .venv\Scripts\python.exe run_seed.py

Nao precisa instalar nada: usa o psycopg2 que ja esta na venv do projeto.
"""
import os
import sys

import psycopg2

SQL_FILE = "seed_render.sql"


def main():
    url = os.environ.get("DATABASE_URL")
    if not url and len(sys.argv) > 1:
        url = sys.argv[1]

    if not url:
        print("ERRO: defina a variavel DATABASE_URL ou passe a URL como argumento.")
        print('Ex.: $env:DATABASE_URL = "postgresql://user:senha@host/db"')
        sys.exit(1)

    if not os.path.exists(SQL_FILE):
        print(f"ERRO: arquivo {SQL_FILE} nao encontrado nesta pasta.")
        sys.exit(1)

    with open(SQL_FILE, "r", encoding="utf-8") as fh:
        sql = fh.read()

    print("Conectando no banco...")
    # autocommit=True deixa o BEGIN/COMMIT que ja existe dentro do .sql controlar a transacao
    conn = psycopg2.connect(url, sslmode="require")
    conn.autocommit = True
    try:
        with conn.cursor() as cur:
            print(f"Executando {SQL_FILE}...")
            cur.execute(sql)
            # Confere o que entrou
            cur.execute("""
                SELECT
                    (SELECT COUNT(*) FROM marketplace_app_user)    AS usuarios,
                    (SELECT COUNT(*) FROM marketplace_app_listing) AS anuncios,
                    (SELECT COUNT(*) FROM marketplace_app_order)   AS pedidos
            """)
            usuarios, anuncios, pedidos = cur.fetchone()
        print("\nSeed aplicado com sucesso!")
        print(f"  Usuarios: {usuarios}")
        print(f"  Anuncios: {anuncios}")
        print(f"  Pedidos:  {pedidos}")
        print("\nSenha de todos os usuarios: senha123")
    except Exception as exc:
        print("\nFALHOU. Nada foi gravado (transacao revertida).")
        print(f"Erro: {exc}")
        sys.exit(1)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
