# 🛍️ LuStyle Management API

Bem-vindo ao repositório da LuStyle Management API! Esta é uma API RESTful desenvolvida com FastAPI para gerenciar clientes, produtos e pedidos de uma loja.

✨ Funcionalidades
Autenticação de Usuários: Registro e login de usuários com JWT (JSON Web Tokens).

Gestão de Clientes (CRUD):

Criar novos clientes.

Listar todos os clientes.

Obter detalhes de um cliente específico.

Atualizar informações de clientes.

Excluir clientes.

Gestão de Produtos (CRUD):

Criar novos produtos.

Listar todos os produtos.

Obter detalhes de um produto específico.

Atualizar informações de produtos.

Excluir produtos.

Gestão de Pedidos (CRUD):

Criar novos pedidos (associando clientes e produtos).

Listar todos os pedidos.

Obter detalhes de um pedido específico.

Atualizar informações de pedidos.

Excluir pedidos.

Validação de Dados: Utiliza Pydantic para validação robusta de entrada e saída de dados.

Migrações de Banco de Dados: Gerenciamento de schema do banco de dados com Alembic.

## 🚀 Tecnologias Utilizadas

Framework: FastAPI

ORM: SQLAlchemy

Banco de Dados: PostgreSQL

Autenticação: JWT (JSON Web Tokens) com python-jose e passlib (bcrypt)

Validação de Dados: Pydantic

Servidor ASGI: Uvicorn

Migrações de DB: Alembic

Testes: Pytest

Containerização: Docker & Docker Compose

## 🛠️ Configuração do Ambiente Local (Desenvolvimento/Teste)

Siga estas instruções para configurar e rodar o projeto em sua máquina local.

Pré-requisitos
Certifique-se de ter os seguintes softwares instalados em sua máquina:

Git: Para clonar o repositório.

Docker Desktop: Inclui Docker Engine e Docker Compose.

Download Docker Desktop

Passos para Configuração
Clone o Repositório:

git clone <https://github.com/Drolpg/LuStyle-management-api.git>
cd LuStyle-management-api

Crie o Arquivo de Variáveis de Ambiente:
se preferir Crie um arquivo .env na raiz do projeto (no mesmo nível do docker-compose.yml) e adicione as seguintes variáveis. Estas são as credenciais para o banco de dados e a chave secreta para JWT. atualmente se encontram no .app/core/database.py e app/core/security.py

## Variáveis de Ambiente para a API

DATABASE_URL=postgresql://postgres:postgres@db:5432/lustyle

SECRET_KEY=sua_chave_secreta_muito_segura_aqui # Mude para uma string longa e aleatória

ACCESS_TOKEN_EXPIRE_MINUTES=30 # Tempo de expiração do token em minutos

Importante: A SECRET_KEY deve ser uma string longa e aleatória. Você pode gerar uma usando Python:

import secrets

print(secrets.token_urlsafe(32))

Crie a Pasta de Migrações do Alembic (se não existir):

O Alembic precisa de uma pasta versions dentro do diretório alembic para armazenar os arquivos de migração.

mkdir -p alembic/versions

Construa e Inicie os Contêineres Docker:

Este comando construirá as imagens Docker e iniciará os serviços da API (api) e do banco de dados (db).

docker compose up --build -d

--build: Garante que as imagens sejam reconstruídas com as últimas alterações do código.

-d: Inicia os contêineres em modo "detached" (em segundo plano).

Execute as Migrações do Banco de Dados:

Após os contêineres estarem rodando, execute as migrações do Alembic para criar as tabelas no banco de dados.

docker exec -it lustyle-management-api-api-1 alembic upgrade head

docker exec -it lustyle-management-api-api-1: Executa um comando dentro do contêiner da sua API.

alembic upgrade head: Aplica todas as migrações pendentes.

Acesse a Documentação da API (Swagger UI):

Sua API estará disponível em <http://localhost:8000>. A documentação interativa (Swagger UI) pode ser acessada em:

<http://localhost:8000/docs>

Execute os Testes (Opcional, mas Recomendado):

Para garantir que tudo está funcionando corretamente, você pode rodar os testes:

docker exec -it lustyle-management-api-api-1 pytest tests/

## ☁️ Deploy na AWS EC2 com Docker

Este guia descreve como fazer o deploy da API em uma instância AWS EC2 usando Docker.

Pré-requisitos AWS

Uma conta AWS ativa.

Uma instância EC2 (ex: Ubuntu 22.04 LTS, t2.micro) já provisionada e acessível via SSH.

Conhecimento básico de SSH e linha de comando Linux.

Chave SSH (.pem): Certifique-se de ter sua chave SSH para acessar a instância.

Configuração da Instância EC2

Conecte-se à sua Instância EC2 via SSH:

ssh -i /caminho/para/sua/chave.pem ec2-user@<IP_PUBLICO_DA_SUA_EC2>

(Substitua /caminho/para/sua/chave.pem e <IP_PUBLICO_DA_SUA_EC2>)

Atualize os Pacotes e Instale o Docker:

sudo apt update

sudo apt install -y docker.io docker-compose

Adicione o Usuário ec2-user ao Grupo docker:

Isso permite que você execute comandos Docker sem sudo.

sudo usermod -aG docker ec2-user

Importante: Você precisará sair e reconectar via SSH para que as mudanças no grupo tenham efeito.

Verifique a Instalação do Docker:

Após reconectar, execute:

docker --version

docker compose version

Ambos os comandos devem retornar as versões instaladas.

Configuração do Security Group (Grupo de Segurança)

Certifique-se de que o Security Group associado à sua instância EC2 permite o tráfego nas portas necessárias:

Porta 22 (SSH): Para acesso SSH.

Porta 8000 (HTTP): Para acesso à sua API FastAPI.

No console da AWS, navegue até EC2 > Instâncias.

Selecione sua instância.

Na aba Security, clique no link do Security Group.

Clique em Edit inbound rules (Editar regras de entrada).

Adicione as seguintes regras:

Type: SSH | Port range: 22 | Source: My IP (ou Anywhere se souber os riscos)

Type: Custom TCP | Port range: 8000 | Source: Anywhere (ou seu IP, se preferir restringir)

Clique em Save rules.

Deploy da Aplicação

Clone o Repositório na Instância EC2:

git clone <https://github.com/Drolpg/LuStyle-management-api.git>

cd LuStyle-management-api

Crie o Arquivo de Variáveis de Ambiente (.env):

Repita o passo de criação do .env com as mesmas variáveis usadas localmente.

nano .env

## Cole o conteúdo do seu .env local aqui

DATABASE_URL=postgresql://postgres:postgres@db:5432/lustyle

SECRET_KEY=sua_chave_secreta_muito_segura_aqui

ACCESS_TOKEN_EXPIRE_MINUTES=30

Salve e saia (Ctrl+X, Y, Enter)

Construa e Inicie os Contêineres Docker:

docker compose up --build -d

Isso pode levar alguns minutos, dependendo da velocidade da sua instância e da sua conexão.

Execute as Migrações do Banco de Dados:

docker exec -it lustyle-management-api-api-1 alembic upgrade head

Importante: Se for a primeira vez que você está subindo o projeto na EC2 e o banco de dados está vazio, você pode
precisar gerar a migração inicial primeiro, caso não tenha sido gerada no seu ambiente local ou se houver um problema no histórico. Se o comando acima falhar, tente:

docker exec -it lustyle-management-api-api-1 alembic revision --autogenerate -m "initial_tables_setup" --head=base

Revise o arquivo gerado em alembic/versions/ para garantir que ele cria todas as tabelas.

Em seguida, execute novamente:

docker exec -it lustyle-management-api-api-1 alembic upgrade head

Verifique o Status dos Contêineres:

docker compose ps

Ambos os serviços (api e db) devem estar com status Up.

## Acesse a API Deployada

Sua API estará acessível publicamente no IP público da sua instância EC2 na porta 8000.

A documentação interativa (Swagger UI) pode ser acessada em:

http://<IP_PUBLICO_DA_SUA_EC2>:8000/docs

📚 Documentação da API

Você pode explorar todos os endpoints da API, seus modelos de dados e testá-los diretamente através da interface interativa do Swagger UI:

Documentação Online (Swagger UI): <http://54.205.84.163:8000/docs#/>
