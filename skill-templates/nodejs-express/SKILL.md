---
name: backend-architecture-nodejs-express
description: AI-Optimized TypeScript Express architecture with Zod validation and 3-layer pattern.
---

# Node.js + Express (TypeScript) — AI-Native Scaffolding

## AI Context & Token Optimization

1. **Strict TypeScript Only:** Pure JavaScript is banned. You MUST use strict TypeScript interfaces for all database models, API responses, and request bodies. This prevents AI hallucinations and ensures safe cross-file refactoring.
2. **Zod for Everything:** Use Zod for environment validation, request body validation, and type inference.
3. **Modular Files:** Keep files under 200 lines. The AI context window degrades when reading monolithic controllers.

## Project Structure

```
src/
├── config/              # Environment & app configuration (env.ts)
├── routes/              # Route definitions (thin — no business logic)
├── controllers/         # Request/response handling (Typed req/res)
├── services/            # Business logic (Pure functions, no Express imports)
├── middleware/          # Express middleware (errorHandler.ts, auth.ts)
├── types/               # Shared TypeScript interfaces & Zod schemas
└── server.ts            # Entry point
```

## Architectural Patterns

**3-Layer Architecture:**
`Route -> Controller -> Service`
Routes bind paths to Controllers. Controllers parse typed requests using Zod and pass data to Services. Services execute logic and return typed objects.

**Global Error Handling:**
Wrap all controllers in `express-async-errors`. Throw custom `AppError` classes in services; let the global error middleware format the JSON response. Never write inline `try/catch` in controllers.
