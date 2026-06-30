---
name: mobile-architecture-android-kotlin
description: Jetpack Compose, MVI (UDF), Clean Architecture, Offline-First Room, and Hilt for Android Kotlin
---

# Android (Kotlin) — "Max Power" AI-Driven Architectural Scaffolding

## Modern Project Initiation Guide

When launching an Android Kotlin application (especially high-performance or offline-first apps like Caller ID) from scratch, initialize using the following strict architectural directives:

1. **100% Jetpack Compose UI:** Never generate XML layout files. Use the Material 3 design system exclusively.
2. **Single-Activity Architecture:** Use a single `MainActivity.kt` with a Compose `NavHost` configured for standard type-safe navigation routes.
3. **MVI + UDF + Clean Architecture:** Group packages strictly by feature. Enforce Unidirectional Data Flow. The View sends sealed `Intents` to the ViewModel, which reduces them into a single `UiState` via a reducer function.
   - `domain/` — Contains pure Kotlin models, repository interfaces (ports), and UseCases. No Android framework dependencies.
   - `data/` — Implements repository interfaces. Prioritizes local caching (Room) for Offline-First capabilities, falling back to remote (gRPC/API).
   - `ui/` — Houses Compose screens, individual components, and ViewModels.
4. **Network & Protocol:** Use gRPC via Wire or Ktor for high-performance, low-latency connections, especially over unstable networks.
5. **Kotlin Coroutines & Flow:** Use `StateFlow<UiState>` for rendering state, `SharedFlow` for one-time events, and `viewModelScope` for scoping. Never use LiveData or RxJava.
6. **Dependency Injection:** Hilt is mandatory. Annotate ViewModels with `@HiltViewModel` and inject constructor dependencies using `@Inject`.
7. **Localization (en/fa):** All strings must be declared in `strings.xml`. Persian strings must reside inside `values-fa/strings.xml`. Ensure RTL support using `LocalLayoutDirection` on RTL screens.

## Project Structure

```
com.company.project/
├── di/                          # Hilt DI modules
│   ├── AppModule.kt
│   └── NetworkModule.kt
├── data/                        # Data layer
│   ├── local/                   # Room DAOs, entities
│   │   ├── dao/
│   │   │   └── UserDao.kt
│   │   └── entity/
│   │       └── UserEntity.kt
│   ├── remote/                  # gRPC / Ktor API services
│   │   ├── grpc/
│   │   │   └── UserGrpcService.kt
│   │   └── dto/
│   │       └── UserResponse.kt
│   └── repository/              # Repository implementations
│       └── UserRepositoryImpl.kt
├── domain/                      # Domain layer (pure Kotlin — no Android deps)
│   ├── model/                   # Domain models
│   │   └── User.kt
│   ├── repository/              # Repository interfaces (ports)
│   │   └── UserRepository.kt
│   └── usecase/                 # Use cases
│       └── GetUserUseCase.kt
└── ui/                          # Presentation layer
    ├── theme/                   # Compose theming
    │   ├── Theme.kt
    │   ├── Color.kt
    │   └── Type.kt
    ├── component/               # Reusable composables
    │   └── LoadingIndicator.kt
    └── screen/                  # Screens (one package per feature)
        └── profile/
            ├── ProfileScreen.kt
            └── ProfileViewModel.kt
```

## Naming Conventions

| Artifact               | Convention         | Example                 |
| ---------------------- | ------------------ | ----------------------- |
| Files                  | `PascalCase`       | `UserRepositoryImpl.kt` |
| Classes / Interfaces   | `PascalCase`       | `GetUserUseCase`        |
| Functions / Properties | `camelCase`        | `getUserById`           |
| Constants / Companions | `UPPER_SNAKE_CASE` | `MAX_RETRY_COUNT`       |
| Composable functions   | `PascalCase`       | `ProfileScreen`         |
| XML resources          | `snake_case`       | `activity_main.xml`     |
| Navigation routes      | `camelCase`        | `profile/{userId}`      |

## Architectural Patterns

### Clean Architecture (3-Layer)

```
UI (Compose + ViewModel) → Domain (UseCases + Models) → Data (Repositories + DataSources)
```

- **UI Layer**: Composable screens observe `StateFlow` from ViewModels. No business logic.
- **Domain Layer**: Pure Kotlin module. Contains use cases and repository interfaces. No Android framework imports.
- **Data Layer**: Implements repository interfaces. Coordinates local (Room) and remote (gRPC/Retrofit) data sources with Offline-First priority.

### MVI (Model-View-Intent) with Unidirectional Data Flow

Every screen gets a `ViewModel` that exposes a single `StateFlow<UiState>` and accepts a single `onIntent(intent: ViewIntent)` function. This eliminates race conditions in UI rendering. The ViewModel acts as a reducer: incoming Intents produce new UiState via aggregation over time.

```
User Action → sealed Intent → ViewModel (Reducer) → UseCase → Repository
                                         ↓
                                    StateFlow<UiState>
                                         ↓
                                   Composable Screen
```

```kotlin
// Example MVI Contract
data class CallerIdUiState(
    val phoneNumber: String = "",
    val displayName: String? = null,
    val isLoading: Boolean = false,
    val error: String? = null
)

sealed interface CallerIdIntent {
    data class LookupNumber(val number: String) : CallerIdIntent
    data object Retry : CallerIdIntent
    data object Clear : CallerIdIntent
}

@HiltViewModel
class CallerIdViewModel @Inject constructor(
    private val lookupNumberUseCase: LookupNumberUseCase
) : ViewModel() {

    private val _uiState = MutableStateFlow(CallerIdUiState())
    val uiState: StateFlow<CallerIdUiState> = _uiState.asStateFlow()

    fun onIntent(intent: CallerIdIntent) {
        when (intent) {
            is CallerIdIntent.LookupNumber -> lookupNumber(intent.number)
            CallerIdIntent.Retry -> retry()
            CallerIdIntent.Clear -> clear()
        }
    }

    private fun lookupNumber(number: String) {
        _uiState.update { it.copy(isLoading = true, error = null) }
        viewModelScope.launch {
            lookupNumberUseCase(number)
                .onSuccess { name -> _uiState.update { it.copy(displayName = name, isLoading = false) } }
                .onFailure { e -> _uiState.update { it.copy(error = e.message, isLoading = false) } }
        }
    }
}
```

### Jetpack Compose

- Prefer `StateFlow` over `LiveData` in ViewModels.
- Use `remember`, `LaunchedEffect`, and `derivedStateOf` for local state management.
- Keep composables stateless where possible — hoist state to the ViewModel.
- Use `Modifier` parameters for all reusable composables to allow parent customization.
- Follow Material 3 design with custom theme (Color, Typography, Shapes).

### Kotlin Coroutines & Flows

- Use `viewModelScope.launch` for ViewModel coroutines.
- Prefer `StateFlow` or `SharedFlow` for one-shot event emission (snackbars, navigation).
- Use `Flow.combine`, `flatMapLatest`, and `catch` operators for reactive data streams.
- Never use `GlobalScope`.

### Dependency Injection via Hilt

- Annotate constructors with `@Inject` for simple cases.
- Create `@Module` classes for interfaces and third-party objects (`gRPC/Ktor`, `Room`).
- Scope singletons properly (`@Singleton`, `@ViewModelScoped`, `@ActivityScoped`).

## Testing Strategies

| Layer           | Test Type                  | Framework                     | File Naming                 |
| --------------- | -------------------------- | ----------------------------- | --------------------------- |
| Use cases       | Unit                       | JUnit 5 + Mockito / MockK     | `GetUserUseCaseTest.kt`     |
| ViewModel (MVI) | Unit (Intent injection)    | JUnit 5 + Turbine (for Flows) | `CallerIdViewModelTest.kt`  |
| Repository      | Unit                       | JUnit 5 + MockK               | `UserRepositoryImplTest.kt` |
| UI / Composable | Snapshot / Compose UI Test | Compose Test                  | `ProfileScreenTest.kt`      |

- Use `MockK` (preferred) or `Mockito` for mocking in Kotlin.
- Use **Turbine** library to test `StateFlow` and `SharedFlow` emissions.
- Use Compose UI Test (`createComposeRule`) to verify composable rendering and interactions.
- Run unit tests locally without an emulator — they should be pure JVM tests.
