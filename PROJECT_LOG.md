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

---

## 🏗️ Estrutura do Projeto

```
portfolio-api/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Entry point da aplicação
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       └── __init__.py     # Routers v1 (a implementar)
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py           # ✅ Configurações
│   │   └── database.py         # ✅ Setup SQLAlchemy
│   ├── models/
│   │   └── __init__.py         # Modelos de banco (a implementar)
│   ├── schemas/
│   │   └── __init__.py         # Schemas Pydantic (a implementar)
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
- [ ] Criar modelos de banco de dados em `app/models/`
- [ ] Criar schemas Pydantic em `app/schemas/`
- [ ] Implementar routers em `app/api/v1/`
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
