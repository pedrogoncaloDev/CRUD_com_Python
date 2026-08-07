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

# Comando que será executado quando o container iniciar
CMD gunicorn main:app -b ${FLASK_HOST}:${FLASK_PORT}