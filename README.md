# Chatbot IFES

Sistema de chatbot para consulta a documentos do IFES com **Retrieval-Augmented Generation (RAG)**.

## Visão Geral

- **Backend**: FastAPI (Python) com autenticação JWT
- **Banco de Dados**: PostgreSQL com pgvector para busca vetorial
- **Frontend Mobile**: React Native (JavaScript) com Expo
- **IA**: OpenAI API para embeddings e geração de respostas
- **Arquitetura**: Camadas (Domain → Application → Infrastructure → Presentation)

---

## Estrutura do Projeto

```
├── chatbot/                  # Módulo original (CLI com RAG)
├── backend/                  # API FastAPI (MVP)
│   ├── app/
│   │   ├── main.py           # Entrada da aplicação FastAPI
│   │   ├── config.py         # Configurações via variáveis de ambiente
│   │   ├── database.py       # Engine e sessão do SQLAlchemy
│   │   ├── dependencies.py   # Dependências FastAPI (auth, DB)
│   │   ├── models/           # Modelos SQLAlchemy (DER completo)
│   │   ├── schemas/          # Schemas Pydantic (request/response)
│   │   ├── routers/          # Rotas da API
│   │   ├── services/         # Lógica de negócio
│   │   └── utils/            # Utilitários (security, response)
│   ├── alembic/              # Migrations do banco
│   ├── tests/                # Testes do backend
│   ├── requirements.txt
│   └── Dockerfile
├── mobile/                   # App React Native (Expo)
│   ├── App.js
│   ├── src/
│   │   ├── screens/          # Telas do app
│   │   ├── services/         # Serviços HTTP (API)
│   │   ├── contexts/         # Context API (Auth)
│   │   └── navigation/       # Navegação
│   └── package.json
├── docker-compose.yml        # PostgreSQL + Backend
└── .env.example              # Variáveis de ambiente
```

---

## Modelo de Dados (DER)

### Entidades Principais
- **perfil** — perfis de usuário (administrador, comum)
- **usuario** — usuários do sistema
- **conversa** — sessões de conversa do usuário
- **pergunta** — perguntas feitas pelo usuário
- **resposta** — respostas geradas pela IA
- **avaliacao** — avaliações das respostas (nota + comentário)
- **categoria** — categorias de documentos
- **documento** — documentos cadastrados
- **versao_documento** — versionamento de documentos
- **documento_resposta** — relação documento × resposta
- **log_administrativo** — logs de ações administrativas

### Extensões para Embeddings
- **documento_chunk** — chunks de texto extraídos de versões de documentos
- **embedding_chunk** — vetores de embedding (pgvector) dos chunks
- **resposta_fonte** — fontes (chunks) usadas para gerar cada resposta
- **indexacao_job** — controle de jobs de indexação

---

## Rotas da API

### Autenticação
| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/api/auth/login` | Login (retorna JWT) |
| GET | `/api/auth/me` | Dados do usuário autenticado |

### Usuários (Admin)
| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/api/usuarios/` | Criar usuário |
| GET | `/api/usuarios/` | Listar usuários |
| GET | `/api/usuarios/{id}` | Buscar usuário |
| PUT | `/api/usuarios/{id}` | Atualizar usuário |
| DELETE | `/api/usuarios/{id}` | Desativar usuário |

### Conversas
| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/api/conversas/` | Iniciar conversa |
| GET | `/api/conversas/` | Listar conversas |
| GET | `/api/conversas/{id}` | Detalhe da conversa |
| GET | `/api/conversas/{id}/historico` | Histórico de perguntas/respostas |
| POST | `/api/conversas/{id}/perguntar` | Enviar pergunta (RAG) |

### Documentos (Admin para mutações)
| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/api/documentos/` | Criar documento |
| GET | `/api/documentos/` | Listar documentos |
| GET | `/api/documentos/{id}` | Detalhes com versões |
| PUT | `/api/documentos/{id}` | Atualizar (nova versão) |
| DELETE | `/api/documentos/{id}` | Desativar documento |
| POST | `/api/documentos/{id}/indexar` | Reindexar embeddings |
| POST | `/api/documentos/categorias` | Criar categoria |
| GET | `/api/documentos/categorias` | Listar categorias |

### Avaliações
| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/api/avaliacoes/` | Avaliar resposta |
| GET | `/api/avaliacoes/{id}` | Buscar avaliação |

### Administração
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/api/admin/metricas` | Métricas do sistema |
| GET | `/api/admin/logs` | Logs administrativos |

---

## Como Executar

### Pré-requisitos
- Docker e Docker Compose
- Python 3.12+
- Node.js 18+ (para o mobile)

### 1. Subir o banco de dados e backend com Docker

```bash
cp .env.example .env
# Edite .env com suas configurações (OPENAI_API_KEY, SECRET_KEY, etc.)

docker compose up -d
```

### 2. Executar migrations

```bash
cd backend
pip install -r requirements.txt
alembic upgrade head
```

### 3. Iniciar o backend (desenvolvimento local)

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

A API estará disponível em `http://localhost:8000` com documentação em `http://localhost:8000/docs`.

### 4. Iniciar o mobile

```bash
cd mobile
npm install
npx expo start
```

### 5. Executar testes

```bash
# Testes do módulo original
pytest tests/ -v

# Testes do backend
cd backend
pytest tests/ -v
```

---

## Variáveis de Ambiente

| Variável | Default | Descrição |
|----------|---------|-----------|
| `DATABASE_URL` | `postgresql://chatbot:chatbot_secret@localhost:5432/chatbot_db` | URL do PostgreSQL |
| `SECRET_KEY` | `dev-secret-key-change-in-production` | Chave para assinar JWT |
| `ALGORITHM` | `HS256` | Algoritmo JWT |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `60` | Expiração do token |
| `OPENAI_API_KEY` | *(obrigatório)* | Chave da API OpenAI |
| `EMBEDDING_MODEL` | `text-embedding-3-small` | Modelo de embedding |
| `CHAT_MODEL` | `gpt-4o-mini` | Modelo de chat |
| `EMBEDDING_DIMENSION` | `1536` | Dimensão do vetor |
| `TOP_K` | `5` | Chunks retornados na busca |
| `CHUNK_SIZE` | `500` | Tamanho do chunk em caracteres |
| `CHUNK_OVERLAP` | `50` | Sobreposição entre chunks |

---

## Fluxo do Usuário Comum

1. Faz login (`POST /api/auth/login`)
2. Inicia conversa (`POST /api/conversas/`)
3. Envia pergunta (`POST /api/conversas/{id}/perguntar`)
4. Recebe resposta com fontes
5. Avalia resposta (`POST /api/avaliacoes/`)
6. Consulta histórico (`GET /api/conversas/{id}/historico`)

## Fluxo do Administrador

1. Faz login
2. Cadastra usuários (`POST /api/usuarios/`)
3. Cadastra documentos (`POST /api/documentos/`)
4. Atualiza documentos (gera nova versão) (`PUT /api/documentos/{id}`)
5. Aciona reindexação (`POST /api/documentos/{id}/indexar`)
6. Consulta métricas (`GET /api/admin/metricas`)
7. Consulta logs (`GET /api/admin/logs`)

---

## Módulo Original (CLI)

O módulo original em `chatbot/` continua funcionando como CLI para testes locais:

```bash
pip install -r requirements.txt
export OPENAI_API_KEY="sk-..."
python main.py
```

| Comando | Ação |
|---------|------|
| Qualquer texto | Pergunta ao chatbot via RAG |
| `/index <texto>` | Indexa novo conhecimento |
| `quit` / `exit` / `q` | Sair |
