# CRUD com Python

![Vue.js](https://img.shields.io/badge/Vue.js-3.x-4FC08D?logo=vuedotjs)
![Vuetify](https://img.shields.io/badge/Vuetify-3.x-1867C0?logo=vuetify)
![Flask](https://img.shields.io/badge/Flask-2.x-000000?logo=flask)
![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python)

## 📌 Visão Geral

Projeto desenvolvido para consolidar meus conhecimentos em desenvolvimento full-stack, implementando um CRUD de usuários com Flask (Python) no backend e Vue.js/Vuetify no frontend.
- **Frontend**: Vue.js 3 + Vuetify 3 (componentes Material Design)
- **Backend**: Flask (Python) com rotas RESTful
- **Banco de Dados**: Postgres 16

## 🚀 Como Executar o Projeto

### Pré-requisitos
- Node.js (v20.12.2+)
- Python (v3.13.2+)
- npm (v10.7.0+)
- pip (v24.3.1+)
- PostgreSQL 16

### 🔧 Instalação

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/Pedro-Gonsalo/CRUD-com-Python.git
   cd CRUD_com_python

2. **Instale as dependências do frontend**:
    ```bash
    cd frontend
    npm install

3. **Instale as dependências do backend: Execute os seguintes comandos para instalar as dependências necessárias no Python:**:
   ```bash
    pip install psycopg2
    pip install flask
    pip install flask-cors
    pip install pytz

4. **Configure o arquivo config_db.py: No diretório backend, edite o arquivo config_db.py com as configurações do seu PostgreSQL 16. Exemplo:**:
    ```bash
    conn_info = {
        "host": "localhost",
        "database": "crud_com_python",
        "user": "seu_usuario",
        "password": "sua_senha",
        "port": "5432"
    }

    conn_database_crud_com_python = {
        "host": "localhost",
        "database": "crud_com_python",
        "user": "seu_usuario",
        "password": "sua_senha",
        "port": "5432"
    }

5. **Inicie o projeto:**
    1. *No frontend, execute:*
        ```bash
        npm run serve
    
    2. *No backend, execute o arquivo api.py:*
        ```bash
            python api.py

## Rotas da API

| Método | Endpoint       | Body (JSON)           | Ação                     |
|--------|----------------|-----------------------|--------------------------|
| GET    | `/users`       | -                     | Lista todos usuários     |
| POST   | `/users`       | `{"nome" : "Novo Nome","email" : "teste1111@email.com.br","senha" : "senha123"}`  | Cria novo usuário        |
| PUT    | `/users/`      | `{"id" : 1,"nome" : "teste","email" : "teste@email.com","senha" : "senha123"}`  | Atualiza usuário         |
| DELETE | `/users/{id}`  | -                     | Remove usuário           |

## Estrutura do projeto
├── backend/                  # Backend Flask<br>
│   ├── __pycache__/<br>
│   ├── api.py                # Rotas da API<br>
│   ├── config_db.py          # Configurações de conexão com o banco de dados<br>
│   ├── database.py           # Arquivo com os métodos para criar o DB e a tabela de usuários <br>
│   ├── users.py              # Arquivo com a classe de usuario<br>
│   ├── utils.py              # Utilitários do back-end<br>
│<br>
├── frontend/                 # Frontend Vue.js<br>
│   ├── public/<br>
│   ├── src/<br>
│   │   ├── components/<br>
│   │   │   └── Home.vue # Página com a tabela para realizar o CRUD <br>
│   │   ├── modais/<br>
│   │   │   ├── AddUserModal.vue  # Modal para adicionar um usuário <br>
│   │   │   ├── EditUserModal.vue  # Modal para editar o usuário <br>
│   │   │   ├── DeleteUserModal.vue # Modal para deletar um usuário <br>
│   │   ├── utils.js # Utilitários do front-end<br>
│   │   ├── App.vue<br>
│   │   └── main.js<br>
│   ├── babel.config.js<br>
│   ├── vue.config.js<br>
│   ├── package.json<br>
│   └── package-lock.json<br>
│
├── .gitignore<br>
└── README.md<br>
