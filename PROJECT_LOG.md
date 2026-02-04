# Portfolio API - Log de Desenvolvimento

> **Última atualização:** 2026-02-03

## 📋 Índice
- [Visão Geral](#visão-geral)
- [Histórico de Desenvolvimento](#histórico-de-desenvolvimento)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Configurações](#configurações)
- [Próximos Passos](#próximos-passos)

---

## 🎯 Visão Geral

**Nome do Projeto:** Portfolio API  
**Tipo:** REST API Backend  
**Framework:** FastAPI  
**Banco de Dados:** PostgreSQL  
**Versão da API:** v1

### Objetivo
API backend profissional para gerenciamento de portfólio, construída com FastAPI seguindo as melhores práticas de desenvolvimento.

---

## 📅 Histórico de Desenvolvimento

### 2026-02-03 - Inicialização do Projeto

**Git Commits:**
- `5ccc5d0` - feat(core): add application settings with pydantic-settings
- `15b43ba` - feat(core): configure SQLAlchemy engine and session
- `8721234` - feat(api): setup FastAPI application with CORS and health check

**Resumo da Implementação:**

Esta fase inicial estabeleceu toda a fundação da API Portfolio:

1. **Infraestrutura Base** - Estrutura de pastas profissional, configuração com pydantic-settings, e setup completo do SQLAlchemy com dependency injection.

2. **Modelo de Dados** - Entidade `Project` completa com 14 campos, incluindo metadados, URLs, tech stack (usando PostgreSQL ARRAY), tipos de projeto, status, e timestamps automáticos. Índices criados em `title` e `slug` para otimização de queries.

3. **Schemas de Validação** - Conjunto completo de schemas Pydantic v2 para diferentes casos de uso: criação, atualização completa, atualização parcial, e respostas públicas. Validações incluem regex patterns, limites de tamanho, e campos obrigatórios vs opcionais.

4. **API REST Completa** - 6 endpoints implementados:
   - `GET /api/v1/projects` - Listagem com filtros (project_type, status, featured) e paginação
   - `GET /api/v1/projects/{id}` - Busca por ID
   - `POST /api/v1/projects` - Criação com geração automática de slug
   - `PUT /api/v1/projects/{id}` - Atualização completa
   - `PATCH /api/v1/projects/{id}` - Atualização parcial
   - `DELETE /api/v1/projects/{id}` - Remoção

5. **Utilitários** - Função `generate_slug()` para converter títulos em slugs URL-friendly, com remoção de acentos, normalização Unicode, e tratamento de caracteres especiais.

6. **Qualidade de Código** - Type hints completos, docstrings detalhadas, tratamento de erros com HTTPException (404, 400), validação de slug único, e padrão de dependency injection.

7. **Docker & Containerização** - Setup completo para desenvolvimento com Docker:
   - Dockerfile multi-stage otimizado para produção
   - docker-compose.yml com PostgreSQL 15 e API
   - Health checks para database e aplicação
   - Hot reload para desenvolvimento
   - Volume persistente para dados do PostgreSQL
   - docker-compose.override.yml.example com pgAdmin
   - .dockerignore para builds otimizados
   - README.md completo com instruções Docker


#### ✅ Estrutura Base Criada
- **Pastas criadas:**
  - `app/api/v1/` - Rotas da API versão 1
  - `app/core/` - Configurações e utilitários centrais
  - `app/models/` - Modelos SQLAlchemy
  - `app/schemas/` - Schemas Pydantic
  - `app/db/` - Utilitários de banco de dados
  - `alembic/versions/` - Migrações do banco de dados
  - `tests/` - Testes automatizados

#### ✅ Arquivos Core Implementados

**1. `app/core/config.py`**
- Configuração usando `pydantic-settings`
- Carregamento automático de variáveis de ambiente via `.env`
- Variáveis configuradas:
  - `API_V1_PREFIX` - Prefixo das rotas da API
  - `PROJECT_NAME` - Nome do projeto
  - `DEBUG` - Modo de depuração
  - `DATABASE_URL` - String de conexão PostgreSQL
  - `SECRET_KEY` - Chave secreta para JWT
  - `ALGORITHM` - Algoritmo de criptografia (HS256)
  - `ACCESS_TOKEN_EXPIRE_MINUTES` - Tempo de expiração do token
  - `BACKEND_CORS_ORIGINS` - Lista de origens permitidas para CORS
- Validador customizado para CORS origins (aceita string separada por vírgulas)

**2. `app/core/database.py`**
- Engine SQLAlchemy configurado com:
  - `pool_pre_ping=True` - Verifica conexões antes de usar
  - `echo=DEBUG` - Log de queries SQL em modo debug
- `SessionLocal` - Factory para criar sessões de banco de dados
- `Base` - Classe base declarativa para modelos
- `get_db()` - Dependency injection para FastAPI (padrão yield)

**3. `app/main.py`**
- Aplicação FastAPI inicializada
- CORS middleware configurado dinamicamente
- Endpoint de health check: `GET /health`
  - Retorna: `{"status": "healthy", "service": "Portfolio API"}`
- Preparado para incluir routers (comentado para futura implementação)

#### ✅ Arquivos de Configuração

**`.env.example`**
- Template completo de variáveis de ambiente
- Valores padrão e exemplos fornecidos
- Instruções para configuração de produção

**`requirements.txt`**
- Dependências Python já existentes:
  - `fastapi[all]==0.115.0`
  - `sqlalchemy==2.0.35`
  - `alembic==1.13.3`
  - `psycopg2-binary==2.9.9`
  - `pydantic-settings==2.5.2`
  - `python-jose[cryptography]==3.3.0`
  - `passlib[bcrypt]==1.7.4`
  - `python-multipart==0.0.12`
  - `python-dotenv==1.0.0`

**`.gitignore`**
- Configurado para ignorar:
  - Arquivos Python compilados
  - Ambientes virtuais
  - Variáveis de ambiente (.env)
  - Arquivos de IDE
  - Bancos de dados locais
  - Cache de testes
  - Logs

#### ✅ Entidade Project Implementada

**1. `app/models/project.py`**
- Modelo SQLAlchemy completo para projetos de portfólio
- Campos implementados:
  - `id` - Primary key com autoincrement
  - `title` - String(200), not null, indexed
  - `slug` - String(200), unique, not null, indexed
  - `short_description` - String(500) para resumo
  - `long_description` - Text para descrição em markdown
  - `tech_stack` - ARRAY(String) para lista de tecnologias (PostgreSQL)
  - `project_type` - String(50) com tipos: data_engineering, ml_ai, web, automation, saas
  - `status` - String(20) com valores: active, archived, draft (default: active)
  - `github_url` - String(500), nullable
  - `demo_url` - String(500), nullable
  - `image_url` - String(500), nullable
  - `featured` - Boolean, default=False
  - `created_at` - DateTime com default func.now()
  - `updated_at` - DateTime com default func.now() e onupdate
- Índices criados em `title` e `slug` para performance
- `__repr__` implementado para debugging

**2. `app/schemas/project.py`**
- Schemas Pydantic v2 completos:
  - `ProjectBase` - Schema base com campos compartilhados e validações
  - `ProjectCreate` - Para criação (POST), sem id e timestamps
  - `ProjectUpdate` - Para atualização (PATCH/PUT), todos campos opcionais
  - `ProjectInDB` - Representação completa do banco com `from_attributes=True`
  - `ProjectPublic` - Schema de resposta pública (herda de ProjectInDB)
  - `ProjectListResponse` - Schema para listagem paginada
- Validações implementadas:
  - Tamanhos mínimos e máximos de strings
  - Regex patterns para `project_type` e `status`
  - Validação de URLs
  - Campos obrigatórios vs opcionais

**3. Exports configurados:**
- `app/models/__init__.py` - Exporta `Project`
- `app/schemas/__init__.py` - Exporta todos os schemas do projeto

#### ✅ API REST Implementada

**1. `app/api/v1/projects.py`**
- Router FastAPI completo com todos os endpoints CRUD:
  - `GET /api/v1/projects` - Listar projetos com filtros e paginação
    - Query params: `skip`, `limit`, `project_type`, `status`, `featured`
    - Ordenação por `created_at` descendente
  - `GET /api/v1/projects/{project_id}` - Buscar projeto por ID
  - `POST /api/v1/projects` - Criar novo projeto (retorna 201)
    - Geração automática de slug a partir do título
    - Validação de slug único
  - `PUT /api/v1/projects/{project_id}` - Atualização completa
  - `PATCH /api/v1/projects/{project_id}` - Atualização parcial
  - `DELETE /api/v1/projects/{project_id}` - Deletar projeto (retorna 204)
- Tratamento de erros completo:
  - HTTPException 404 para recursos não encontrados
  - HTTPException 400 para slugs duplicados
- Type hints completos em todos os endpoints
- Docstrings detalhadas com exemplos de uso
- Dependency injection com `get_db()`

**2. `app/core/utils.py`**
- Função `generate_slug(text: str) -> str`:
  - Remove acentos usando normalização Unicode
  - Converte para lowercase
  - Substitui espaços por hífens
  - Remove caracteres especiais
  - Remove hífens duplicados
  - Exemplos: "My Project" → "my-project", "Análise de Dados" → "analise-de-dados"

**3. `app/main.py`**
- Router de projects incluído na aplicação
- Prefix: `/api/v1/projects`
- Tag: `projects` para documentação automática

---

## 🏗️ Estrutura do Projeto

```
portfolio-api/
├── app/
│   ├── __init__.py
│   ├── main.py                 # ✅ Entry point com routers
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── projects.py     # ✅ Endpoints REST
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py           # ✅ Configurações
│   │   ├── database.py         # ✅ Setup SQLAlchemy
│   │   └── utils.py            # ✅ Funções auxiliares
│   ├── models/
│   │   ├── __init__.py         # ✅ Exports
│   │   └── project.py          # ✅ Modelo Project
│   ├── schemas/
│   │   ├── __init__.py         # ✅ Exports
│   │   └── project.py          # ✅ Schemas Project
│   └── db/
│       └── __init__.py         # Utilitários DB (a implementar)
├── alembic/
│   └── versions/               # Migrações (a criar)
├── tests/
│   └── __init__.py             # Testes (a implementar)
├── .env.example                # ✅ Template de variáveis
├── .gitignore                  # ✅ Configurado
├── requirements.txt            # ✅ Dependências
└── PROJECT_LOG.md              # ✅ Este arquivo
```

**Legenda:**
- ✅ Implementado
- 🔄 Em desenvolvimento
- ⏳ Planejado

---

## 🛠️ Tecnologias Utilizadas

### Backend
- **FastAPI 0.115.0** - Framework web moderno e rápido
- **Python 3.x** - Linguagem de programação
- **Uvicorn** - Servidor ASGI

### Banco de Dados
- **PostgreSQL** - Banco de dados relacional
- **SQLAlchemy 2.0.35** - ORM Python
- **Alembic 1.13.3** - Gerenciador de migrações

### Segurança
- **Python-JOSE** - Implementação JWT
- **Passlib** - Hashing de senhas (bcrypt)

### Configuração
- **Pydantic Settings 2.5.2** - Gerenciamento de configurações type-safe
- **Python-dotenv** - Carregamento de variáveis de ambiente

---

## ⚙️ Configurações

### Variáveis de Ambiente Necessárias

```env
# API
API_V1_PREFIX=/api/v1
PROJECT_NAME=Portfolio API
DEBUG=False

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/portfolio_db

# Security
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
BACKEND_CORS_ORIGINS=http://localhost:3000,http://localhost:8000
```

### Como Executar

1. **Criar ambiente virtual:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```

2. **Instalar dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar ambiente:**
   ```bash
   cp .env.example .env
   # Editar .env com suas configurações
   ```

4. **Executar aplicação:**
   ```bash
   uvicorn app.main:app --reload
   ```

5. **Acessar:**
   - API: http://localhost:8000
   - Health Check: http://localhost:8000/health
   - Docs: http://localhost:8000/docs

---

## 🎯 Próximos Passos

### Prioridade Alta
- [x] Criar modelos de banco de dados em `app/models/`
- [x] Criar schemas Pydantic em `app/schemas/`
- [x] Implementar routers em `app/api/v1/`
- [ ] Configurar Alembic para migrações
- [ ] Criar primeira migração do banco de dados

### Prioridade Média
- [ ] Implementar autenticação JWT
- [ ] Criar middleware de autenticação
- [ ] Adicionar validações de permissões
- [ ] Implementar testes unitários
- [ ] Configurar CI/CD

### Prioridade Baixa
- [ ] Documentação da API
- [ ] Logs estruturados
- [ ] Monitoramento e métricas
- [ ] Docker e docker-compose
- [ ] Deploy em produção

---

## 📝 Notas Técnicas

### Padrões Adotados
- **Type Hints:** Uso completo de type hints em todo o código
- **Docstrings:** Documentação em todas as funções e classes
- **Dependency Injection:** Uso de FastAPI Depends para injeção de dependências
- **Separation of Concerns:** Separação clara entre camadas (routes, schemas, models, core)

### Decisões Arquiteturais
1. **Versionamento de API:** Estrutura preparada para múltiplas versões (`/api/v1/`)
2. **Configuração Centralizada:** Todas as configs em `app/core/config.py`
3. **Session Management:** Uso de context manager para sessões de banco de dados
4. **CORS Flexível:** Configuração via variável de ambiente para diferentes ambientes
5. **PostgreSQL ARRAY:** Uso de `ARRAY(String)` para `tech_stack` ao invés de JSON para melhor performance em queries

---

## 🔄 Atualizações

Este arquivo será atualizado conforme o projeto evolui. Cada nova feature, mudança arquitetural ou decisão importante será documentada aqui.

**Formato de atualização:**
```markdown
### YYYY-MM-DD - Título da Atualização
- Descrição das mudanças
- Arquivos afetados
- Decisões técnicas
```
