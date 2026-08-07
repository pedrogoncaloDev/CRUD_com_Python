# UserHub

[![Vue.js](https://img.shields.io/badge/Vue.js-3.x-4FC08D?logo=vuedotjs)](https://vuejs.org/)
[![Vuetify](https://img.shields.io/badge/Vuetify-3.x-1867C0?logo=vuetify)](https://vuetifyjs.com/)
[![Flask](https://img.shields.io/badge/Flask-2.x-000000?logo=flask)](https://flask.palletsprojects.com/)
[![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?logo=postgresql)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker)](https://www.docker.com/)
[![CI](https://github.com/pedrogoncaloDev/UserHub/actions/workflows/ci.yml/badge.svg)](https://github.com/pedrogoncaloDev/UserHub/actions/workflows/ci.yml)

## 📋 Sobre o Projeto

Sistema completo de gerenciamento de usuários (CRUD) desenvolvido para consolidar conhecimentos em desenvolvimento full-stack. O projeto implementa uma arquitetura moderna com separação entre frontend e backend, oferecendo uma interface intuitiva e responsiva para gerenciar usuários.

### ✨ Funcionalidades

- ✅ Listagem de usuários
- ➕ Cadastro de novos usuários
- ✏️ Edição de informações de usuários
- 🗑️ Exclusão de usuários
- 🔍 Interface responsiva com Material Design
- 🐳 Suporte para Docker

### 🛠️ Tecnologias Utilizadas

**Frontend:**
- Vue.js 3.x
- Vuetify 3.x (Material Design)
- Axios para requisições HTTP

**Backend:**
- Flask 2.x (Python)
- Flask-CORS
- Psycopg2 (PostgreSQL adapter)

**Banco de Dados:**
- PostgreSQL 16

**DevOps:**
- Docker & Docker Compose

---

## 🚀 Como Executar o Projeto

Existem **duas formas** de executar o projeto:

1. **[Com Docker](#-opção-1-executar-com-docker-recomendado)** (Recomendado) - Mais rápido e sem necessidade de configurações manuais
2. **[Manualmente](#-opção-2-executar-manualmente)** - Controle total sobre cada componente

---

## 🐳 Opção 1: Executar com Docker (Recomendado)

### Pré-requisitos

- [Docker](https://docs.docker.com/get-docker/) instalado
- [Docker Compose](https://docs.docker.com/compose/install/) instalado

### Passos para Executar

1. **Clone o repositório:**

```bash
git clone https://github.com/pedrogoncaloDev/UserHub.git
cd UserHub
```

2. **Configure as variáveis de ambiente:**

Crie um arquivo `.env` na raiz do projeto baseado no `.env.example`:

```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas credenciais:

```env
DB_NAME=userhub
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_PORT=5432
```

3. **Inicie os containers:**

```bash
docker-compose up -d
```

Este comando irá:
- Baixar as imagens necessárias
- Criar e configurar o banco de dados PostgreSQL
- Construir e iniciar o backend Flask
- Construir e iniciar o frontend Vue.js

4. **Acesse a aplicação:**

- **Frontend:** http://localhost:8080
- **Backend API:** http://localhost:5000

5. **Para parar os containers:**

```bash
docker-compose down
```

**Para parar e remover volumes (dados do banco):**

```bash
docker-compose down -v
```

---

## 💻 Opção 2: Executar Manualmente

### Pré-requisitos

- **Node.js** v20.12.2 ou superior
- **npm** v10.7.0 ou superior
- **Python** 3.13.2 ou superior
- **pip** v24.3.1 ou superior
- **PostgreSQL** 16

### Configuração do Banco de Dados

1. **Instale o PostgreSQL 16**

2. **Crie o banco de dados:**

```sql
CREATE DATABASE userhub;
```

### Configuração do Backend

1. **Configure as variáveis de ambiente:**

Crie um arquivo `.env` na raiz do projeto baseado no `.env.example`:

```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas credenciais:

```env
DB_NAME=userhub
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_PORT=5432
```

2. **Navegue até a pasta do backend:**

```bash
cd back_end
```

3. **Crie e ative o ambiente virtual:**

**Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source ./venv/bin/activate
```

4. **Instale as dependências:**

```bash
pip install -r requirements.txt
```

5. **Configure o interpretador Python no VS Code (opcional):**

- Pressione `Ctrl + Shift + P` (Windows/Linux) ou `Cmd + Shift + P` (Mac)
- Digite `Python: Select Interpreter`
- Selecione o interpretador do ambiente virtual (`./venv/Scripts/python` ou `./venv/bin/python`)

6. **Execute o backend:**

```bash
python api.py
```

O backend estará rodando em: http://localhost:5000

### Configuração do Frontend

1. **Em um novo terminal, navegue até a pasta do frontend:**

```bash
cd front_end
```

2. **Instale as dependências:**

```bash
npm install
```

3. **Execute o frontend:**

```bash
npm run serve
```

O frontend estará rodando em: http://localhost:8080

---

## 📡 Documentação da API

### Endpoints Disponíveis

| Método | Endpoint | Body (JSON) | Descrição |
|--------|----------|-------------|-----------|
| **GET** | `/users` | - | Retorna todos os usuários |
| **POST** | `/users` | `{"nome": "João Silva", "email": "joao@email.com", "senha": "senha123"}` | Cria um novo usuário |
| **PUT** | `/users` | `{"id": 1, "nome": "João Silva", "email": "joao@email.com", "senha": "novaSenha123"}` | Atualiza um usuário existente |
| **DELETE** | `/users/{id}` | - | Remove um usuário pelo ID |

### Exemplos de Requisições

**Listar todos os usuários:**
```bash
curl http://localhost:5000/users
```

**Criar um novo usuário:**
```bash
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{"nome":"Maria Santos","email":"maria@email.com","senha":"senha123"}'
```

**Atualizar um usuário:**
```bash
curl -X PUT http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{"id":1,"nome":"Maria Silva","email":"maria.silva@email.com","senha":"novaSenha123"}'
```

**Deletar um usuário:**
```bash
curl -X DELETE http://localhost:5000/users/1
```

---

## ✅ Testes

O projeto conta com testes automatizados no backend e no frontend, executados automaticamente via CI (GitHub Actions) a cada push/PR para a branch `main`.

### Backend (pytest)

Os testes ficam em `back_end/tests/` e cobrem a API (`test_api.py`), o modelo de usuário (`test_users.py`), a configuração do banco de dados (`test_config_db.py`) e as funções auxiliares (`test_utils.py`).

```bash
cd back_end

# Ativar o ambiente virtual (veja seção de configuração do backend)
# Instalar dependências, se ainda não instaladas
pip install -r requirements.txt

# Executar todos os testes
pytest -v

# Executar com relatório de cobertura
pytest --cov
```

### Frontend (Jest)

Os testes ficam em `front_end/tests/unit/` e cobrem componentes (`Home`, `Grid`, `AddUser`, `EditUserModal`, `DeleteUserModal`) e funções utilitárias (`utils`, `validationRules`).

```bash
cd front_end

# Instalar dependências, se ainda não instaladas
npm install

# Executar os testes
npm test
```

### CI (GitHub Actions)

O workflow definido em `.github/workflows/ci.yml` roda os testes de backend e frontend em paralelo a cada `push`/`pull_request` para `main`, e só marca o pipeline como aprovado (`ci-gate`) se ambos passarem.

---

## 📁 Estrutura do Projeto

```
UserHub/
├── .github/
│   └── workflows/
│       └── ci.yml               # Pipeline de CI (testes backend + frontend)
│
├── back_end/                    # Backend Flask
│   ├── __pycache__/
│   ├── tests/                   # Testes automatizados (pytest)
│   │   ├── conftest.py
│   │   ├── test_api.py          # Testes das rotas da API
│   │   ├── test_config_db.py    # Testes da configuração do banco
│   │   ├── test_users.py        # Testes do modelo de usuário
│   │   └── test_utils.py        # Testes das funções auxiliares
│   ├── api.py                   # Rotas da API REST
│   ├── config_db.py             # Configurações do banco de dados
│   ├── database.py              # Métodos de criação do DB e tabelas
│   ├── users.py                 # Classe e modelo de usuário
│   ├── utils.py                 # Funções auxiliares
│   ├── Dockerfile               # Configuração Docker do backend
│   └── requirements.txt         # Dependências Python
│
├── front_end/                   # Frontend Vue.js
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   └── Home.vue         # Componente principal com tabela CRUD
│   │   ├── modais/
│   │   │   ├── AddUserModal.vue    # Modal de adição de usuário
│   │   │   ├── EditUserModal.vue   # Modal de edição de usuário
│   │   │   └── DeleteUserModal.vue # Modal de confirmação de exclusão
│   │   ├── App.vue              # Componente raiz
│   │   ├── main.js              # Configuração inicial do Vue
│   │   ├── utils.js             # Funções auxiliares
│   │   └── validationRules.js   # Regras de validação de formulários
│   ├── tests/
│   │   └── unit/                # Testes automatizados (Jest)
│   │       ├── Home.spec.js
│   │       ├── Grid.spec.js
│   │       ├── AddUser.spec.js
│   │       ├── EditUserModal.spec.js
│   │       ├── DeleteUserModal.spec.js
│   │       ├── utils.spec.js
│   │       └── validationRules.spec.js
│   ├── babel.config.js
│   ├── vue.config.js
│   ├── package.json
│   ├── Dockerfile               # Configuração Docker do frontend
│   └── nginx.conf               # Configuração Nginx para produção
│
├── demonstracao/                # Screenshots e demonstrações
├── .env.example                 # Exemplo de variáveis de ambiente
├── .gitignore
├── docker-compose.yml           # Orquestração dos containers
└── README.md
```

---

## 🔧 Comandos Úteis

### Docker

```bash
# Iniciar containers
docker-compose up -d

# Ver logs dos containers
docker-compose logs -f

# Ver logs de um serviço específico
docker-compose logs -f backend
docker-compose logs -f frontend

# Parar containers
docker-compose stop

# Remover containers
docker-compose down

# Remover containers e volumes (apaga dados do banco)
docker-compose down -v

# Rebuildar as imagens
docker-compose build

# Rebuildar e iniciar
docker-compose up -d --build
```

### Frontend (modo desenvolvimento)

```bash
# Instalar dependências
npm install

# Executar em modo desenvolvimento
npm run serve

# Compilar para produção
npm run build

# Lint e correção de código
npm run lint

# Executar testes (Jest)
npm test
```

### Backend

```bash
# Ativar ambiente virtual (Windows)
.\venv\Scripts\activate

# Ativar ambiente virtual (Linux/Mac)
source ./venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Executar servidor
python api.py

# Executar testes (pytest)
pytest -v

# Desativar ambiente virtual
deactivate
```

---

## 🐛 Troubleshooting

### Problema: Porta já em uso

Se as portas 5000, 8080 ou 5432 já estiverem em uso:

1. Pare os serviços que estão usando essas portas, ou
2. Altere as portas no `docker-compose.yml` ou nas configurações manuais

### Problema: Erro de conexão com o banco de dados

1. Verifique se o PostgreSQL está rodando
2. Confirme as credenciais no arquivo `.env`
3. Verifique se o banco de dados `userhub` foi criado

### Problema: Frontend não conecta com Backend

1. Verifique se o backend está rodando na porta 5000
2. Confirme se o CORS está configurado corretamente no `api.py`
3. Verifique a URL da API no código do frontend

---

## 📝 Notas de Desenvolvimento

- O projeto utiliza CORS para permitir requisições do frontend para o backend
- Modo debug está ativado no Flask (desabilite em produção)

---

## 🚧 Próximas Melhorias

- [ ] Paginação na listagem de usuários (Busca do back-end trazendo todos os usuários)
- [ ] Filtros e busca avançada (melhorar porque hj só filtra o objeto no front-end)
- [x] Testes unitários e de integração
- [x] CI/CD pipeline (testes automatizados)
- [ ] Documentação Swagger/OpenAPI

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fazer um fork do projeto
2. Criar uma branch para sua feature (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abrir um Pull Request