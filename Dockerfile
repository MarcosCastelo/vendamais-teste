# Use a imagem oficial do Python como imagem base
FROM python:latest

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app
RUN apt-get update \
  && apt-get -y install libpq-dev gcc \
  && pip install --upgrade pip

# Copia os arquivos de requisitos e instala as dependências do projeto
COPY requirements.txt /app/
RUN pip install -r requirements.txt
# Copia o projeto para o diretório de trabalho
COPY . /app/
