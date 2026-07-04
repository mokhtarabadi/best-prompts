---
name: backend-architecture-fastapi
description: AI-Optimized FastAPI architecture with strict Pydantic V2 schemas and modular routing.
---

# FastAPI (Python) — AI-Native Scaffolding

## AI Context & Token Optimization

1. **Strict Type Hinting:** Python's dynamic nature causes AI hallucinations. You MUST use strict type hints (`-> dict`, `: str`) on every single function, argument, and return type.
2. **Pydantic V2 First:** Lean heavily on Pydantic. It is the most token-efficient way for an AI to understand data structures.
3. **Low Boilerplate:** FastAPI is chosen for its minimal boilerplate. Do not over-engineer abstractions. Keep dependency injection (`Depends()`) simple and localized.

## Project Structure

```
app/
├── api/                 # API routers (v1/users.py)
├── core/                # config.py (Pydantic BaseSettings)
├── db/                  # Database session and setup (Supabase/Postgres)
├── models/              # SQLAlchemy 2.0 Typed Models
├── schemas/             # Pydantic V2 Models (DTOs)
├── services/            # Business logic
└── main.py              # FastAPI instance
```

## Architectural Patterns

**Dependency Injection:** Use `Depends()` for database sessions (`get_db`) and authentication (`get_current_user`).
**ORM to Schema Separation:** Never return SQLAlchemy models directly from endpoints. Always return Pydantic schemas to ensure data validation and hide sensitive fields.
