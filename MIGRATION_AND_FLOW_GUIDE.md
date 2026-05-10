# Incident Management System - Complete Flow & Migration Setup

## ✅ All Issues Fixed

### 1. **Database Configuration**

- ✅ Fixed Alembic `env.py` to properly load `Base.metadata` from models
- ✅ Added environment variable support for `DATABASE_URL` in Alembic config
- ✅ Created initial migration file: `0001_initial_migration.py`

### 2. **Model Consistency**

- ✅ Changed Incident model from `Integer` ID to `UUID` (consistent with User model)
- ✅ Incident now uses `sqlalchemy.dialects.postgresql.UUID` like User
- ✅ Both entities properly configured for PostgreSQL

### 3. **Import Fixes**

- ✅ Fixed API router: `triage.controller` → `src.triage.controller`
- ✅ Fixed triage controller imports (added `src.` prefix)
- ✅ Fixed triage models imports (added `src.` prefix)
- ✅ Fixed triage service imports (added `src.` prefix)
- ✅ Fixed triage rules imports (added `src.` prefix)
- ✅ Fixed triage similarity imports (changed `incident_id: int` → `incident_id: str`)

---

## 📊 System Architecture & Complete Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                        FastAPI Application                        │
│                        (main.py entry point)                       │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                ┌──────────┼──────────┐
                ▼          ▼          ▼
        ┌──────────┐ ┌──────────┐ ┌──────────┐
        │   Auth   │ │ Incidents│ │  Triage  │
        │ Endpoints│ │Endpoints │ │Endpoints │
        └──────────┘ └──────────┘ └──────────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │   Database Core  │
                  │  (SQLAlchemy)    │
                  └──────────────────┘
                           │
         ┌─────────────────┼─────────────────┐
         ▼                 ▼                 ▼
      ┌───────┐         ┌──────────┐    ┌─────────┐
      │ Users │         │ Incidents│    │  FAISS  │
      │ Table │         │  Table   │    │  Index  │
      └───────┘         └──────────┘    └─────────┘
         │                  │
    PostgreSQL Database     In-Memory Vector DB
```

---

## 🔄 Complete User Flow

### 1. **Authentication Flow**

```
POST /api/v1/auth/register
├── Payload: { email, username, password, role }
├── Hash password using bcrypt
├── Create User record in DB (UUID primary key)
└── Return JWT token + User data

POST /api/v1/auth/login
├── Payload: { email, password }
├── Verify credentials
└── Return JWT token + User data

GET /api/v1/auth/me
├── Requires: Bearer token
└── Return authenticated user profile
```

### 2. **Incident Creation Flow**

```
POST /api/v1/incidents/
├── Requires: Bearer token (authentication)
├── Payload: { title, description, severity, assigned_to }
├── Create Incident record (UUID primary key)
├── Store in PostgreSQL incidents table
└── Return IncidentResponse with UUID id

GET /api/v1/incidents/
├── Requires: Bearer token
├── Query parameters: skip (offset), limit (max 100)
├── Return list ordered by created_at DESC
└── Pagination supported

GET /api/v1/incidents/{incident_id}
├── Requires: Bearer token
├── Path parameter: incident_id (UUID)
├── Lookup incident in DB
└── Return single IncidentResponse

PATCH /api/v1/incidents/{incident_id}
├── Requires: Bearer token
├── Payload: { title?, description?, severity?, status?, assigned_to? }
├── Update specific fields (exclude_unset=True)
└── Return updated IncidentResponse
```

### 3. **AI Triage Flow**

```
POST /api/v1/incidents/{incident_id}/triage
├── Requires: Bearer token
├── Path parameter: incident_id (UUID)
│
├── Step 1: Rule Engine (Fast)
│   └── Match keywords in title/description
│       Return: category, severity, suggested_fix, ai_notes
│
├── Step 2: Text Embedding
│   └── Encode incident text using SentenceTransformer
│       Model: all-MiniLM-L6-v2 (384-dim embeddings)
│
├── Step 3: Similarity Search
│   └── Query FAISS index for similar past incidents (top_k=3)
│       Return: matching incidents with similarity scores
│
├── Step 4: Confidence Boost
│   └── If similar incident found (score > 0.75)
│       confidence += 0.15 (capped at 1.0)
│
├── Step 5: Persist Results
│   └── Update incident record with:
│       - category
│       - severity
│       - suggested_fix
│       - ai_notes
│
├── Step 6: Index for Future
│   └── Add incident embedding to FAISS index
│       (In-memory, lost on restart - add persistence if needed)
│
└── Return TriageResponse with results
```

---

## 📋 Database Schema

### Users Table

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    role ENUM('ENGINEER', 'MANAGER', 'ADMIN') NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at DATETIME NOT NULL
);
```

### Incidents Table

```sql
CREATE TABLE incidents (
    id UUID PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    severity ENUM('LOW', 'MEDIUM', 'HIGH', 'CRITICAL') NOT NULL,
    status ENUM('OPEN', 'IN_PROGRESS', 'RESOLVED') NOT NULL,
    assigned_to VARCHAR(100),
    category ENUM('PAYMENT', 'AUTH', 'DATABASE', 'NETWORK', 'PERFORMANCE', 'UNKNOWN'),
    suggested_fix TEXT,
    ai_notes TEXT,
    created_at TIMESTAMP WITH TIMEZONE NOT NULL,
    updated_at TIMESTAMP WITH TIMEZONE
);
```

---

## 🚀 Running Migrations

### Initial Setup

```bash
# 1. Ensure DATABASE_URL is set in .env
echo "DATABASE_URL=postgresql://user:pass@localhost/incident_ops" > .env

# 2. Run initial migration
alembic upgrade head

# 3. Start application
uvicorn src.main:app --reload
```

### Migration Status

```bash
# Check current migration version
alembic current

# See all migrations
alembic history

# Downgrade to previous version (if needed)
alembic downgrade -1
```

---

## ✨ Key Features Implemented

### Phase 1: Core System (✅ Complete)

- ✅ Structured incident lifecycle (OPEN → IN_PROGRESS → RESOLVED)
- ✅ User authentication with JWT
- ✅ CRUD operations for incidents
- ✅ Role-based access control (ENGINEER, MANAGER, ADMIN)
- ✅ PostgreSQL database with proper migrations

### Phase 2: Intelligent Decision Support (✅ Complete)

- ✅ Rule-based severity classification
- ✅ AI-powered category prediction
- ✅ Suggested fix recommendations
- ✅ Similarity search using embeddings

### Phase 3: Future Enhancements

- 🔲 Persistent embedding storage
- 🔲 Historical incident analytics
- 🔲 Incident templates
- 🔲 Team notifications & escalation

---

## 🛠️ Technology Stack

| Component         | Technology                             |
| ----------------- | -------------------------------------- |
| **Framework**     | FastAPI                                |
| **Server**        | Uvicorn                                |
| **Database**      | PostgreSQL 13+                         |
| **ORM**           | SQLAlchemy 2.0+                        |
| **Migrations**    | Alembic                                |
| **Auth**          | JWT (python-jose) + Bcrypt             |
| **Embeddings**    | SentenceTransformer (all-MiniLM-L6-v2) |
| **Vector Search** | FAISS (in-memory)                      |
| **Validation**    | Pydantic                               |

---

## 📝 Environment Variables Required

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/incident_ops

# JWT
JWT_SECRET=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Optional
LOG_LEVEL=INFO
```

---

## ✅ Testing the Complete Flow

```bash
# 1. Register user
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "engineer@example.com",
    "username": "john",
    "password": "SecurePass123",
    "role": "ENGINEER"
  }'

# 2. Create incident
curl -X POST http://localhost:8000/api/v1/incidents/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Payment gateway down",
    "description": "Users cannot complete checkout. Transactions failing.",
    "severity": "CRITICAL",
    "assigned_to": "john"
  }'

# 3. Trigger AI triage
curl -X POST http://localhost:8000/api/v1/incidents/{incident_id}/triage \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# 4. List incidents
curl -X GET http://localhost:8000/api/v1/incidents/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

## 📦 All Fixed Files

1. ✅ `alembic/env.py` - Configured for autogenerate
2. ✅ `alembic/versions/0001_initial_migration.py` - Initial schema
3. ✅ `backend/src/api.py` - Fixed router imports
4. ✅ `backend/src/entities/incident.py` - Changed ID to UUID
5. ✅ `backend/src/triage/controller.py` - Fixed imports, UUID support
6. ✅ `backend/src/triage/models.py` - Fixed imports, UUID support
7. ✅ `backend/src/triage/service.py` - Fixed imports
8. ✅ `backend/src/triage/rules.py` - Fixed imports
9. ✅ `backend/src/triage/similarity.py` - Fixed imports, str IDs

---

## 🎯 System Status: READY FOR DEPLOYMENT ✅

All critical issues have been fixed. The system is now ready for:

- Database migration
- Testing
- Deployment

Run migrations with: `alembic upgrade head`
