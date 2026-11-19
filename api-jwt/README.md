# Atividade Prática — Autenticação com JWT em API Flask

API Flask com autenticação via **JWT (JSON Web Token)**, usando `Flask-JWT-Extended`.
O login valida usuário e senha e devolve um token; rotas protegidas só respondem com um token válido.

## Estrutura

```
api-jwt/
├── app.py             # aplicação Flask
├── demo.py            # demonstração das rotas (para print/evidência)
├── requirements.txt   # dependências
└── README.md          # este arquivo
```

## Tecnologias

- Python 3.12
- Flask 3.1
- Flask-JWT-Extended 4.7
- Werkzeug (hash de senhas)

## Como executar

No terminal, a partir da pasta `api-jwt`:

```powershell
# 1. (caso ainda não exista) criar o ambiente virtual na raiz do projeto
python -m venv venv

# 2. ativar o ambiente
# PowerShell:
..\venv\Scripts\Activate.ps1
# Prompt de Comando (cmd):
..\venv\Scripts\activate

# 3. instalar as dependências
pip install Flask Flask-JWT-Extended

# 4. executar a API
python app.py
```

A API sobe em `http://127.0.0.1:5000/`.

## Configuração

```python
app.config["JWT_SECRET_KEY"] = "chave-secreta-da-aula"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)
```

- `JWT_SECRET_KEY`: chave usada para assinar os tokens.
- `JWT_ACCESS_TOKEN_EXPIRES`: validade do token (30 minutos).

> Em produção, a chave secreta deve vir de uma variável de ambiente, e não do código.

## Usuários de teste

| Usuário    | Senha | Perfil     | Nome                |
|------------|-------|------------|---------------------|
| `carolina` | 1234  | professora | Carolina Cardinale  |
| `ana`      | abcd  | aluna      | Ana Souza           |

As senhas são armazenadas como **hash** (`generate_password_hash`), nunca em texto puro.

## Endpoints

| Método | Rota             | Protegida | Descrição                                  |
|--------|------------------|-----------|--------------------------------------------|
| GET    | `/`              | Não       | Rota inicial (mensagem da API)             |
| POST   | `/login`         | Não       | Valida credenciais e retorna o `access_token` |
| GET    | `/perfil`        | Sim       | Dados do usuário autenticado               |
| GET    | `/area-restrita` | Sim       | Desafio: mensagem de boas-vindas           |

### Exemplos

**1. Rota inicial**

`GET /`
```json
{ "mensagem": "API de autenticação com JWT" }
```

**2. Login**

`POST /login`
```json
{ "usuario": "carolina", "senha": "1234" }
```
Resposta `200`:
```json
{
  "mensagem": "Login realizado com sucesso",
  "access_token": "<token>"
}
```
Credenciais inválidas retornam `401`:
```json
{ "erro": "Usuário ou senha inválidos" }
```

**3. Perfil (protegida)**

`GET /perfil` com cabeçalho `Authorization: Bearer <token>`
```json
{
  "usuario": "carolina",
  "nome": "Carolina Cardinale",
  "perfil": "professora"
}
```
Sem token, a resposta é `401`:
```json
{ "msg": "Missing Authorization Header" }
```

**4. Área restrita (desafio)**

`GET /area-restrita` com cabeçalho `Authorization: Bearer <token>`
```json
{ "mensagem": "Bem-vindo à área restrita, carolina!" }
```

## Testando no Bruno

1. Crie uma requisição **POST** para `http://127.0.0.1:5000/login`.
2. Em **Body**, escolha **JSON** e envie:
   ```json
   { "usuario": "carolina", "senha": "1234" }
   ```
3. Copie o valor do campo `access_token`.
4. Crie uma requisição **GET** para `http://127.0.0.1:5000/perfil`.
5. Em **Auth**, selecione **Bearer Token** e cole o token.
6. Envie — a resposta trará os dados da Carolina.

O Bruno enviará o cabeçalho:
```
Authorization: Bearer <token>
```

## Demonstração (evidência de funcionamento)

Para gerar um print único mostrando a API funcionando, execute:

```powershell
python demo.py
```

O script percorre todas as rotas e mostra o status e a resposta de cada uma:

| Passo | Rota | Resultado esperado |
|-------|------|--------------------|
| 1 | `GET /` | 200 — mensagem da API |
| 2 | `POST /login` (válido) | 200 — `access_token` |
| 3 | `GET /perfil` (sem token) | 401 — `Missing Authorization Header` |
| 4 | `GET /perfil` (com token) | 200 — dados da Carolina |
| 5 | `GET /area-restrita` (com token) | 200 — mensagem de boas-vindas |
| 6 | `POST /login` (senha errada) | 401 — usuário ou senha inválidos |

## Fluxo da autenticação

1. O cliente envia usuário e senha para `/login`.
2. A API valida as credenciais e gera o JWT.
3. O cliente guarda o token temporariamente.
4. Nas rotas protegidas, o cliente envia `Authorization: Bearer <token>`.
5. A API valida o token antes de liberar o recurso.
