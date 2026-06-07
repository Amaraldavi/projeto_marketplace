#!/usr/bin/env bash
# Script de build usado pelo Render (Build Command: ./build.sh)
# Encerra na primeira falha.
set -o errexit

pip install -r requirements.txt

# Coleta os estáticos (WhiteNoise comprime e versiona)
python manage.py collectstatic --no-input

# Aplica as migrações no banco
python manage.py migrate
