# ADR-002: Separate backend (FastAPI) and frontend (React) deployment

## Status

Accepted <!-- Proposed | Accepted | Rejected | Deprecated | Superseded -->

## Date

2026-06-25

## Context

The legacy system, built using Django, does not have a complete implementation of the user interface. Most of the existing UI was built with server-rendered Django views (Templates), which tightly couples presentation logic to the backend framework and limits the flexibility to evolve the frontend independently.

As part of the broader migration effort defined in [ADR-001](#), the system is being restructured into a Modular Monolith. Although the resulting system remains a monolith from a codebase and deployment-unit perspective at the module level, the intent of this decision is to keep the **UI layer and the backend API deployment independent from each other**, without introducing the full complexity of a distributed architecture.

This separation is driven by three main goals:

1. Avoid a disruptive, all-at-once rewrite of the legacy system by decoupling the interface concern from the backend migration effort described in ADR-001.
2. Replace Django's server-rendered views with a dedicated frontend framework, enabling a modern, component-based, and maintainable UI.
3. Achieve minimal decoupling between UI and backend so that each can be built, tested, versioned, and deployed independently, without requiring a full microservices infrastructure.

## Decision

We will use **FastAPI** for the backend API and **React** for the frontend user interface, deployed as two independent artifacts that communicate exclusively through a well-defined HTTP/REST contract.

## Alternatives Considered

### Backend

#### Option A: FastAPI (Selected)

**Pros**

- **Native async support:** Built on Starlette and ASGI, allowing high-throughput, non-blocking I/O — well suited for an API-first backend consumed by a decoupled frontend.
- **Automatic API contract generation:** Built-in OpenAPI/Swagger and Pydantic-based schema validation reduce the effort of documenting and versioning the API consumed by React.
- **Clean alignment with the Modular Monolith:** FastAPI's lightweight, unopinionated structure makes it straightforward to expose each business module (defined in ADR-001) through its own router/interface without inheriting Django's MTV conventions.
- **Type safety and validation:** Pydantic models enforce strict input/output contracts, reducing integration bugs between backend and frontend teams.
- **Performance:** Generally lower request latency and higher concurrency ceiling than Django's synchronous WSGI stack for I/O-bound workloads typical of a JSON API.

**Cons**

- Smaller built-in ecosystem compared to Django (no built-in Admin, ORM, or Auth system out of the box); these need to be assembled from third-party libraries (e.g., SQLAlchemy, Alembic, `fastapi-users`).
- Requires the team to build conventions from scratch (project structure, dependency injection patterns, error handling) that Django provided implicitly.
- Introduces a second stack to operate and monitor alongside the existing Django codebase during the transition period.

#### Option B: Reformulate Django REST Framework (DRF) on the legacy system

**Pros**

- **Legacy continuity:** Reuses the existing Django models, ORM, and Auth system already in place, avoiding a full backend rewrite.
- **Mature ecosystem:** DRF provides serializers, permissions, and browsable API tooling that are battle-tested and well documented.
- **Lower short-term learning curve:** The team is already familiar with Django's conventions.

**Cons**

- **High existing technical debt:** The legacy codebase carries significant "spaghetti code," with business logic, database access, and view/serialization concerns heavily intertwined. Reformulating it into a clean REST layer would require substantial refactoring effort with high risk of dragging the same coupling issues into the new API layer.
- **Contradicts the Modular Monolith goals from ADR-001:** Django's MTV pattern and tightly coupled ORM make it harder to enforce the strict module boundaries already decided upon.
- **Synchronous-first architecture:** Django's traditional WSGI request-handling model is less naturally suited to high-concurrency, I/O-bound API workloads compared to an ASGI-based alternative.

#### Option C: API in .NET

**Pros**

- **Strong typing and tooling:** C#'s static typing, along with mature tooling (Visual Studio, Rider) and the .NET ecosystem, offers robust support for building large-scale APIs.
- **High raw performance:** ASP.NET Core is competitive in benchmarks for throughput and latency, particularly for CPU-bound workloads.
- **Enterprise-grade libraries:** Built-in support for dependency injection, background workers, and a mature ORM (Entity Framework Core).

**Cons**

- **Full stack and language discontinuity:** Introducing .NET would require the team to maintain two entirely different language ecosystems (Python for the existing modules/tools and C# for the new API), increasing onboarding cost and reducing code/knowledge reuse from ADR-001.
- **No reuse of existing Python-based domain logic:** Any business logic already modeled in Python during the Modular Monolith migration would need to be reimplemented, duplicating effort already invested.
- **Increased operational footprint:** Adds a new runtime and deployment pipeline (CLR/.NET) to an infrastructure that is otherwise Python-centric, with no clear technical justification given the current scope.

### Frontend

#### Option A: Vanilla JS + Bootstrap

**Pros**

- **Minimal footprint:** No build tooling, framework runtime, or additional dependencies required.
- **Low learning curve:** Straightforward for developers with basic JS/HTML/CSS knowledge.
- **Fast initial setup:** Bootstrap provides ready-made UI components, accelerating the first iterations.

**Cons**

- **Poor scalability for UI complexity:** Without a component model or state-management abstraction, the interface tends to degrade into the same kind of unstructured, tightly coupled code the team is actively trying to move away from (per ADR-001's motivations).
- **Manual DOM management:** Increases the risk of bugs and inconsistent UI state as the number of views and interactions grows.
- **Limited long-term maintainability:** Lacks the tooling ecosystem (testing, component reuse, type safety) needed to support a UI that is expected to grow alongside the backend modules.

#### Option B: Vue.js

**Pros**

- **Gentle learning curve:** Simpler mental model than React for teams new to component-based frontend development.
- **Built-in reactivity and tooling:** Official router, state management (Pinia/Vuex), and CLI reduce initial setup decisions.
- **Good documentation and progressive adoption:** Can be introduced incrementally into an existing page if needed.

**Cons**

- **Smaller ecosystem and hiring pool** compared to React, particularly relevant for long-term maintainability and team scaling.
- **Fewer enterprise-grade component libraries** and third-party integrations relative to React's ecosystem.

#### Option C: React (Selected)

**Pros**

- **Component-based architecture:** Naturally aligns with the modular, bounded-context approach adopted for the backend in ADR-001, enabling a similarly decoupled UI structure (feature-based component organization).
- **Largest ecosystem and community:** Broad availability of libraries (routing, state management, forms, data fetching) and a large talent pool, reducing hiring and onboarding risk.
- **Strong tooling maturity:** Well-established patterns for testing, type safety (via TypeScript), and integration with OpenAPI-generated clients (which pairs naturally with FastAPI's automatic schema generation).
- **Flexibility:** Unopinionated core library allows the team to adopt only the pieces it needs (routing, state management) rather than a full framework, keeping the frontend deployment lightweight and independent.

**Cons**

- Requires more upfront architectural decisions (state management, routing, project structure) than Vue, since React is a library rather than a full framework.
- Steeper learning curve for developers unfamiliar with JSX and the broader React ecosystem conventions.

## Consequences

### Positive

- **Independent deployability:** The frontend (React) and backend (FastAPI) can be built, versioned, and deployed on independent pipelines, reducing release coupling and blast radius.
- **Clear contract boundary:** All communication is mediated through a documented REST API (OpenAPI-generated from FastAPI), enforcing a strict separation between presentation and business logic — consistent with the module boundary principles established in ADR-001.
- **Technology fit for purpose:** FastAPI's async, schema-driven design and React's component model are both suited to supporting the modular backend structure without introducing Django's MTV coupling issues.
- **Incremental migration path:** UI screens can be migrated from Django templates to React incrementally, without requiring the full backend migration to be completed first.

### Negative / Trade-offs

- **Two independent stacks to operate:** The team must maintain build, test, and deployment pipelines for both a Python/FastAPI service and a JavaScript/React application, increasing operational surface area compared to a single Django deployment.
- **API contract discipline required:** Any breaking change to the FastAPI schema must be carefully versioned and communicated, since the frontend no longer shares a codebase (and therefore no compile-time coupling) with the backend.
- **Cross-Origin/Auth complexity:** Separating deployments introduces the need to explicitly manage CORS, authentication token handling (e.g., JWT), and environment-specific API base URLs, which were previously implicit in a server-rendered Django setup.
- **Duplicated concerns:** Certain validation and formatting logic may need to exist on both sides (FastAPI/Pydantic and React forms), requiring discipline to keep them consistent.

### Items to Monitor

- **API Contract Stability:** Track breaking vs. non-breaking changes to the FastAPI OpenAPI schema to prevent unannounced frontend regressions.
- **Build and Deployment Pipeline Health:** Monitor build times and deployment frequency for both the React and FastAPI pipelines to ensure the separation is not introducing release friction.
- **Authentication/Session Flow:** Closely monitor the token-based auth flow between React and FastAPI during the transition away from Django's session-based auth, given this is a new failure surface.
- **Legacy UI Migration Progress:** Track the proportion of screens still served by Django templates versus those migrated to React, to ensure the transition does not stall indefinitely.

## References

- ADR-001: Adopt a modular monolith architecture
- FastAPI Documentation — https://fastapi.tiangolo.com
- React Documentation — https://react.dev
- OpenAPI Specification
- Domain-Driven Design (DDD) Bounded Contexts