# Usa uma imagem leve do Python
FROM python:3.12-slim

# Define a pasta onde o código vai rodar
WORKDIR /app

# Copia os arquivos de dependências
COPY requirements.txt .

# Instala as dependências
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copia o restante do código pra dentro do container
COPY . .

# Cria um usuário não-root para rodar a aplicação
RUN useradd -m appuser
USER appuser

# Valores padrão pensados para uso via docker-compose;
# sobrescrevíveis por variáveis de ambiente em outros ambientes de deploy
ENV FLASK_HOST=0.0.0.0
ENV FLASK_PORT=5000

# Sem isso, o stdout do Python fica bufferizado quando não há TTY (como em
# "docker compose logs"), então prints como "Aguardando debugger..." somem
ENV PYTHONUNBUFFERED=1

# --timeout 0 desativa o timeout de worker do gunicorn (padrão 30s):
# sem isso, o worker é morto e reiniciado enquanto o debugpy.listen()
# aguarda o VS Code conectar (ou enquanto um breakpoint fica pausado),
# entrando em loop de restart e nunca permitindo anexar o debugger.
#
# -X frozen_modules=off: desde o Python 3.11 os módulos "frozen" ficam
# ativos por padrão, o que impede o debugpy de setar breakpoints
# corretamente (a variável de ambiente PYTHON_FROZEN_MODULES=off não
# tem efeito aqui, só a flag de linha de comando funciona). Por isso o
# gunicorn é chamado via "python -m gunicorn" em vez do entrypoint direto.
CMD python3 -X frozen_modules=off -m gunicorn main:app -b ${FLASK_HOST}:${FLASK_PORT} --timeout 0