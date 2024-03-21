# Vendamais Teste

Este projeto é uma API REST desenvolvida com Django Rest Framework, configurada para ser executada em containers Docker. A API oferece funcionalidades básicas de um sistema bancário, incluindo registro e login de usuários, bem como operações de depósito, saque, transferência entre contas e geração de relatórios de transações.

## Começando

Para iniciar o projeto, você precisará ter o Docker e o Docker Compose instalados em sua máquina. Com essas dependências instaladas, você pode configurar e executar o projeto seguindo os passos abaixo.

### Configuração

1. Clone o repositório do projeto para sua máquina local:

```bash
git clone https://github.com/MarcosCastelo/vendamais-teste.git
cd vendamais-teste
```

2. Construa os containers Docker e inicie os serviços:

```bash
docker-compose up --build
```

Após a construção e inicialização dos containers, a API estará acessível através da porta configurada (por padrão, `8000`).

## Endpoints da API

A API oferece os seguintes endpoints:

### Contas

- **Registro de Usuário**

  `POST /api/accounts/register`

  Payload:

  ```json
  {
    "username": "seu_usuario",
    "cpf": "00000000000",
    "password": "sua_senha",
    "email": "seu_email@example.com"
  }
  ```

- **Login**

  `POST /api/accounts/login`

  Payload:

  ```json
  {
    "username": "seu_usuario",
    "password": "sua_senha"
  }
  ```

### Transações

(Necessário autenticação)

- **Depósito**

  `POST /api/transactions/deposito`

  Payload:

  ```json
  {
    "amount": 100.00
  }
  ```

- **Saque**

  `POST /api/transactions/withdraw`

  Payload:

  ```json
  {
    "amount": 50.00
  }
  ```

- **Transferência**

  `POST /api/transactions/transfer`

  Payload:

  ```json
  {
    "destination_cpf": "cpf_destinatario",
    "amount": 75.00
  }
  ```

- **Relatório de Transações**

  `GET /api/transactions/report`

  Não é necessário payload. O endpoint retorna um relatório das transações do usuário autenticado.

## Autenticação

Os endpoints de transações requerem autenticação. Após realizar o login, um token será fornecido. Esse token deve ser incluído no cabeçalho das requisições para os endpoints autenticados, seguindo o formato:

```
Authorization: Bearer <SEU_TOKEN>
```

## Tecnologias Utilizadas

- Django Rest Framework: Framework para criação de APIs REST com Django.
- Docker e Docker Compose: Para containerização e gestão de múltiplos containers.
- PostgreSQL: Banco de dados utilizado para simplificar a configuração e a execução do projeto.
