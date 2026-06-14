# PROJETO MULTIDISCIPLINAR do curso de Análise e Desenvolvimento de Sistemas
# Aluno: Alfonso Aklberto Slovinski Canfild - RU: 351946

# Raízes do Nordeste — API Backend

Esta API foi desenvolvida para o sistema de pedidos da rede **Raízes do Nordeste**, como projeto de TCC do curso de ADS. A ideia aqui é simular o backend de uma operação real de food services: cadastro de produtos, controle de estoque por unidade, criação de pedidos, pagamento (mock), programa de fidelidade e auditoria das ações realizadas no sistema. Tudo conforme regras de negócios.

O projeto em si foi construído com o **FastAPI** + **SQLAlchemy** + **PostgreSQL**, seguindo uma estrutura em camadas (rotas, schemas, modelos e infraestrutura).

---------------------------------------------

## 📋 Sobre o projeto

Esta aplicação (API) cobre o fluxo completo de um pedido:

1. O cliente se cadastra e faz login (autenticação via JWT)
2. Um pedido é criado vinculado a uma unidade e a um canal (app, totem, balcão, pickup ou delivery)
3. Itens são adicionados ao pedido, com baixa automática de estoque
4. O pedido é pago (simulação de pagamento via Mock)
5. O usuário acumula pontos no programa de fidelidade
6. O pedido segue pelos status de preparo até a entrega (ou pode ser cancelado, com devolução do estoque)

Todas essas ações relevantes (criação, atualização, cancelamento) ficam registradas em uma tabela de **auditoria**, com o usuário responsável e o horário da ação.

---------------------------------------------

## 🛠️ Tecnologias utilizadas no projeto

- **Python 3**          — linguagem de programação
- **FastAPI**           — framework principal da API
- **SQLAlchemy**        — ORM para o banco de dados
- **PostgreSQL**        — banco de dados relacional
- **Pydantic**          — validação de dados e schemas
- **python-jose**       — geração e validação de tokens JWT
- **passlib (bcrypt)**  — hash de senhas
- **python-dotenv**     — variáveis de ambiente

---------------------------------------------

## 📂 Estrutura do projeto

backend/
├── app/
│   ├── api/routes/         - Rotas da API (endpoints)
│   ├── core/               - Autenticação, segurança, auditoria e permissões
│   ├── domain/models/      - Modelos do banco de dados (SQLAlchemy)
│   ├── schema/             - Schemas de entrada e saída (Pydantic)
│   ├── infrastructure/     - Conexão com o banco de dados
│   └── main.py             - Ponto de entrada da aplicação
├── .env.example
├── .env
├── .gitignore
└── README.md

---------------------------------------------

## ⚙️ Como rodar o projeto localmente

### 1. Pré-requisitos

Antes de começar, você vai precisar ter instalado:

- [Python 3.11+](https://www.python.org/downloads/)
- [PostgreSQL](https://www.postgresql.org/download/)
- Git (é opcional, caso vá clonar o repositório)

### 2. Clone o repositório

``bash``
git clone <https://github.com/AlfonsoCanfild/TCC-Ra-zes-do-Nordeste>
cd backend

### 3. Crie e ative um ambiente virtual

No Windows:
``bash``
python -m venv venv
venv\Scripts\activate

No Linux/Mac:
``bash``
python -m venv venv
source venv/bin/activate

### 4. Instale as dependências

``bash``
pip install -r requirements.txt

### 5. Configure as variáveis de ambiente

Copie o arquivo de exemplo e ajuste com os seus dados:

``bash``
cp .env.example .env

Abra o `.env` e preencha:

DATABASE_URL=postgresql://postgres:SUASENHA@localhost:5432/raizes_do_nordeste
SECRET_KEY=uma_chave_secreta_qualquer

### 6. Crie o banco de dados

No PostgreSQL, crie um banco vazio com o nome que você definiu no `DATABASE_URL`:

``sql``
CREATE DATABASE raizes_do_nordeste;

As tabelas são criadas automaticamente pelo APP na primeira execução, então não é necessário rodar nenhum script de criação manual.

### 7. Suba a aplicação

``bash``
uvicorn app.main:app --reload

Se tudo der certo, a API estará disponível em:
http://127.0.0.1:8000

E a documentação interativa (Swagger) em:
http://127.0.0.1:8000/docs


---------------------------------------------

## 🔐 Autenticação

A maior parte das rotas exige autenticação via **JWT**, conforme regra de negócios.

O fluxo é:
1. Crie um usuário em `POST /usuarios`
2. Faça login em `POST /auth/login` (envie `email` e `senha`)
3. A resposta traz um `access_token`
4. Use esse token no cabeçalho `Authorization: Bearer <token>` nas demais requisições

### Perfis de usuário

O sistema trabalha com três perfis, que controlam o que cada usuário pode fazer:

|  Perfil   |               Permissões                          |
| `ADMIN`   | Acesso total ao sistema                           |
| `GERENTE` | Gerencia pedidos, estoque e relatórios da unidade |
| `CLIENTE` | Cria pedidos e consulta seus próprios dados       |


---------------------------------------------

## 👤 Criando o usuário ADMIN inicial

Como o `POST /usuarios` exige o token de `ADMIN` para cadastrar novos usuários, é obrigatório criar primeiro o Admin manualmente.

1. Gere o hash da senha desejada rodando no terminal Python (dentro do ambiente virtual):

``python``
from passlib.context import CryptContext
pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
print(pwd.hash("sua_senha_aqui"))

2. Copie o hash gerado e insira no banco via SQL:

``sql``
INSERT INTO usuarios (nome, email, senha, perfil)
VALUES ('Administrador', 'admin@raizesdonordeste.com', '<hash_gerado_aqui>', 'ADMIN');

3. Faça login normalmente em `POST /auth/login` com esse e-mail e senha para gerar o token de administrador.


---------------------------------------------

## 📌 Principais endpoints

| Método | Rota | Descrição |
| `POST` | `/auth/login` | Login e geração de token |
| `POST` | `/usuarios` | Cadastro de usuário (requer ADMIN) |
| `GET` / `POST` / `PUT` / `DELETE` | `/produtos` | CRUD de produtos |
| `GET` / `POST` / `PUT` / `DELETE` | `/unidades` | CRUD de unidades |
| `GET` / `POST` / `PUT` / `DELETE` | `/estoque` | Controle de estoque por unidade |
| `POST` | `/pedidos` | Criação de pedido |
| `GET` | `/pedidos?canalPedido=...&page=...&limit=...` | Listagem com filtro e paginação |
| `PATCH` | `/pedidos/{id}/status` | Atualiza o status do pedido (preparo, pronto, entregue) |
| `PATCH` | `/pedidos/{id}/cancelar` | Cancela o pedido e devolve o estoque |
| `POST` | `/itens-pedido` | Adiciona um item ao pedido |
| `POST` | `/pagamentos/mock` | Simula o pagamento de um pedido |
| `GET` | `/fidelidade/{idUsuario}` | Consulta pontos de fidelidade |
| `GET` | `/fidelidade/ranking` | Ranking de clientes por pontos |
| `GET` | `/auditoria` | Histórico de ações realizadas no sistema |
| `GET` | `/relatorios/vendas` | Relatório de vendas |


---------------------------------------------

## 📄 Licença

Projeto desenvolvido para fins acadêmicos (TCC).
Universidade Uninter Educacional S/A
Alfonso Alberto Slovinski Canfild - RU 351946