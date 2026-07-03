# ADR-001: Adopt a modular monolith architecture
## Status

Accepted <!-- Proposed | Accepted | Rejected | Deprecated | Superseded -->

## Date

2026-06-25

## Context

The legacy system, built using Django, suffered from an unclean architecture and poor practices regarding the standard Model-View-Controller (MVC) pattern. All existing functionalities coexisted tightly coupled within this MVC structure, leading to a "big ball of mud" where business logic, database queries, and presentation rules were heavily intertwined.

Although the system currently has few developed features, the lack of boundaries makes it difficult to maintain and scale. Migrating directly to microservices would introduce premature complexity and infrastructure overhead that the current scope does not justify.

## Decision

We will migrate the legacy Django system to a Modular Monolith Architecture.

Instead of isolating features purely by technical layers (Models/Views), the application will be divided into high-level, vertically sliced modules based on business domains. Each module will encapsulate its own business logic and maintain strict boundaries, communicating with other modules only through well-defined public interfaces (APIs or events).

## Alternatives Considered

### Option A: Modular monolith Architecture (Selected)

**Pros**

- Domain Isolation: Prevents the legacy issue of tangled logic by enforcing strict boundaries between business capabilities.

- Maintainability: Easier to understand, test, and refactor since changes to one module won't unexpectedly break another.

- Microservice Readiness: If a specific module needs to scale independently in the future, its clear boundaries will allow it to be easily extracted into a microservice.

- Low Operational Overhead: Keeps deployment and infrastructure simple compared to a distributed microservices mesh.

**Cons**

- Requires discipline from the team to prevent modules from directly importing each other's internal components and breaking the architectural boundaries.

### Option B: Refactoring the Existing Code with Django

**Pros**

- Legacy Transparency & Low Friction: No requirement for a complete data migration or learning a new language/framework. The transition is smoother for the existing codebase.

- Faster Initial Velocity: Leverages Django’s built-in features (Admin, ORM, Auth) which are already partially implemented, reducing time-to-market for current features.

- Lower Initial Risk: Refactoring in-place avoids the "Second System Syndrome" (the risk of failing entirely while rewriting a system from scratch).

**Cons**

- High Risk of Architectural Drift: Without strict physical boundaries, it is extremely easy for developers to bypass logical layers, eventually falling back into the same chaotic, tightly coupled MVC structure.

- Framework Lock-in & Overhead: Django's tightly integrated ORM and MTV (Model-Template-View) pattern make it difficult to enforce a strict Clean Architecture or separation of concerns.

- Scalability Bottlenecks: Scaling requires scaling the entire monolith, making resource allocation inefficient if only one specific feature suffers from high load.

### Option C: Migrating to a Microservices Architecture

**Pros**

- Absolute Decoupling: Forces strict physical boundaries. It is impossible for one service to directly access the database or logic of another without a network call.

- Independent Scalability & Deployments: Each business capability can be scaled, deployed, and maintained individually without affecting the rest of the system.

- Technology Agnostic: Different services can use different databases or languages if a specific business problem requires it.

**Cons**

- Severe Overengineering: For a system with few developed features that can comfortably coexist in a single relational database, a distributed system adds massive, unjustified complexity.

- High Operational & Infrastructure Overhead: Requires managing container orchestration (like Kubernetes or complex Docker Compose configurations), API Gateways, service discovery, and distributed logging/tracing.

- Distributed Data Complexity: Enforcing data consistency (transactions across services) becomes highly complex, requiring patterns like Saga or CQRS instead of simple database joins.

## Consequences

### Positive

- **Strong Domain Decoupling:** Enforces strict boundaries between business domains, resolving the legacy issue where all features coexisted in a tangled Django MVC structure.
- **Architectural Control and Maintenance:** Easier to test, understand, and refactor separate modules without the risk of breaking unrelated functionalities.
- **Microservice Readiness:** Provides a seamless evolutionary pathway to extract specific modules into independent microservices in the future if scalability demands it.
- **Low Operational Complexity:** Keeps infrastructure, deployment pipelines, and database management simple by avoiding the overhead of a fully distributed system.

### Negative / Trade-offs

- **Strict Code Discipline Required:** The team must actively enforce boundary checks (e.g., using architecture-linter tools) to prevent modules from bypassing public interfaces and importing each other's internal components.
- **Monolithic Release Cycle:** Although internal boundaries are clean, the entire application is still deployed as a single unit, meaning a critical failure at runtime in one module could potentially affect the whole system.

### Items to Monitor

- **Cross-Module Dependency Graph:** Regularly audit internal imports to ensure modules are not becoming tightly coupled over time.
- **Database Connection Pool:** Monitor the single relational database to ensure heavy queries from one domain do not starve the resources of another.
- **Application Startup Time:** Track initialization time as more modules are added to ensure rapid local development and deployments.

## References

- Modular Monolith Architecture Patterns
- Domain-Driven Design (DDD) Bounded Contexts
- Related ADR: ADR-002: Separate backend (FastAPI) and frontend (React) deployment.