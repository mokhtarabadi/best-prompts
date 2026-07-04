---
name: mobile-architecture-android-kotlin
description: Jetpack Compose, MVI (UDF), and Kotlin for token-efficient Android development.
---

# Android (Kotlin) — "Max Power" AI-Driven Architectural Scaffolding

## AI Context & Token Optimization

1. **XML is Strictly Banned:** Never generate `.xml` layout files. XML forces the AI to maintain cross-file context (matching IDs between Kotlin and XML), which wastes tokens and causes layout binding hallucinations.
2. **100% Jetpack Compose:** Write all UI in declarative Kotlin. Compose allows the AI to generate UI and logic in a single, predictable, token-efficient tree.
3. **Modular Composables:** Break large UIs into extremely small, pure `@Composable` functions. The AI struggles to modify 500-line Compose functions without breaking brackets.

## Architectural Patterns

**MVI (Model-View-Intent) + UDF:**
Every screen uses a single `ViewModel`. The ViewModel exposes exactly one `StateFlow<UiState>`. The View sends sealed `Intents` to the ViewModel. This eliminates race conditions and makes the AI's reasoning traceable through a single `when(intent)` reducer block.

**Supabase / BaaS Integration:**
For rapid AI development, prefer direct integration with Supabase/Firebase SDKs in the Data layer to eliminate custom backend boilerplate, unless a dedicated backend is provided.
