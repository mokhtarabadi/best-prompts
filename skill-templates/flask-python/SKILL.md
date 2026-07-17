---
name: flask-python
description: Application Factory, Blueprints, SQLAlchemy, and config separation for Flask
---

# Flask (Python) — Best Practices

## Project Structure

```
project/
├── app/
│   ├── __init__.py           # Application Factory (create_app)
│   ├── config.py             # Configuration classes (Dev, Prod, Test)
│   ├── extensions.py         # Flask extensions (db, migrate, login)
│   ├── blueprints/
│   │   ├── auth/
│   │   │   ├── __init__.py   # Blueprint creation
│   │   │   ├── routes.py     # Route definitions
│   │   │   └── forms.py      # WTForms schemas
│   │   └── users/
│   │       ├── __init__.py
│   │       └── routes.py
│   ├── models/               # SQLAlchemy models
│   │   ├── __init__.py
│   │   └── user.py
│   ├── services/             # Business logic
│   │   └── user_service.py
│   └── templates/            # Jinja2 templates (if server-rendered)
├── tests/
│   ├── conftest.py           # Pytest fixtures (app, client, db)
│   ├── test_auth.py
│   └── test_users.py
├── .env                      # Local environment variables
├── requirements.txt
└── run.py                    # Entry point
```

## Naming Conventions

| Artifact              | Convention          | Example           |
| --------------------- | ------------------- | ----------------- |
| Files/Directories     | `snake_case`        | `user_service.py` |
| Classes               | `PascalCase`        | `UserService`     |
| Functions/Methods     | `snake_case`        | `get_user_by_id`  |
| Variables             | `snake_case`        | `current_user`    |
| Blueprint names       | plural nouns        | `users`           |
| Route prefixes        | plural `kebab-case` | `/api/users`      |
| Environment variables | `UPPER_SNAKE_CASE`  | `DATABASE_URL`    |

## Architectural Patterns

### Application Factory Pattern

Use `create_app(config_name)` in `app/__init__.py` to build the Flask instance. This allows creating different app instances for development, testing, and production without global state.

```python
def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(config_map[config_name])
    register_extensions(app)
    register_blueprints(app)
    return app
```

### Blueprints for Routing

Organize routes into Blueprints. Each feature domain gets its own Blueprint. Never define routes directly on the `app` instance outside of a Blueprint.

```python
users_bp = Blueprint("users", __name__, url_prefix="/api/users")
```

### SQLAlchemy ORM

- Define models in a dedicated `models/` package, not in `routes.py`.
- Use `backref` sparingly — prefer explicit `relationship` definitions.
- Use Alembic (via Flask-Migrate) for all schema migrations; never hand-write DDL.
- Keep query logic in dedicated repository functions or service methods — never inline queries in route handlers.

### Configuration Separation

Create a `config.py` with at least three classes: `Config` (base), `DevelopmentConfig`, `ProductionConfig`, `TestingConfig`. Load the correct one via environment variable or default.

### Virtual Environment Rules

- Always use a virtual environment (venv or pipenv).
- Pin dependency versions in `requirements.txt`.
- Never commit `.venv/` or `__pycache__/` to version control.

## Testing Strategies

| Layer        | Test Type   | Framework                  | File Naming            |
| ------------ | ----------- | -------------------------- | ---------------------- |
| Service      | Unit        | Pytest                     | `test_user_service.py` |
| Route / View | Integration | Pytest + Flask test client | `test_auth_routes.py`  |
| Model        | Unit        | Pytest                     | `test_user_model.py`   |

- Use `pytest` as the test runner (not `unittest`).
- Use `conftest.py` to define shared fixtures (app instance, test client, database session).
- Use an in-memory SQLite database for fast test runs.
- For every Blueprint, write at least one test that validates the route returns the expected status code.
