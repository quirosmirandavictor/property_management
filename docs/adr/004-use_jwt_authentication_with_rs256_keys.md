# ADR-004: Use JWT authentication with RS256 keys

## Status

Accepted <!-- Proposed | Accepted | Rejected | Deprecated | Superseded -->

## Date

2026-06-30

## Context

The system is currently designed as a modular monolith following Clean Architecture principles (see ADR-004: Apply Clean Architecture for each module), with explicit boundaries between modules and dependencies pointing inward toward the domain.

Although the application runs as a single deployable unit today, the architecture is intentionally designed to allow future extraction of modules into independent microservices if business growth or scalability requirements demand it.

Given this, the authentication mechanism must not assume that all modules will always share the same process, database, or trust boundary. An authentication approach tightly coupled to a single shared secret or a centralized session store would work for the monolith today, but would create friction and rework if modules are later split into separately deployed services that need to verify identity independently.

We need an authentication mechanism that:

- Works well within the current modular monolith.
- Does not require significant rearchitecting if modules are extracted into microservices later.
- Allows multiple modules (and potentially future independent services) to verify a user's identity without needing access to sensitive signing material.
- Supports clear separation between the component that issues identity (authentication) and the components that only need to verify it.

## Decision

We will use JWT (JSON Web Token) authentication signed with RS256 (RSA + SHA-256), an asymmetric signing algorithm.

A single component (the authentication module) will hold the RSA private key and will be the only one authorized to issue and sign tokens. All other modules that need to verify a user's identity will do so using the corresponding RSA public key, without ever having access to the private key.

This decouples the *capability to issue tokens* from the *capability to verify tokens*, aligning with the Clean Architecture principle of keeping trust boundaries explicit and dependencies inward-pointing. Within the monolith, this is implemented as an internal authentication module exposing a verification interface (public key / JWKS) to the rest of the modules. If a module is later extracted into a microservice, it can continue verifying tokens the same way, without needing direct access to the authentication module's internals or a shared secret.

## Alternatives Considered

### Option A: JWT with HS256 (shared symmetric key)

**Pros**

- Simpler to configure: a single secret key, no public/private key pair management.
- Computationally cheaper to sign and verify than RS256.
- Sufficient when the issuer and verifier are the same trusted component.

**Cons**

- The same secret must be shared with every module that needs to verify tokens; any module holding it could also *issue* valid tokens, which weakens trust boundaries between modules.
- Poor fit for the intended evolution toward microservices: if modules are extracted, the shared secret would need to be distributed to independently deployed services, increasing the blast radius of a leak.
- Key rotation requires updating the secret everywhere simultaneously, which becomes harder as more services consume it.

### Option B: Opaque sessions with centralized store (Redis/DB)

**Pros**

- Immediate and trivial revocation (deleting the session entry invalidates it instantly).
- Small, meaningless tokens; no signature parsing/verification logic needed in each module.
- Full, real-time control over active sessions (e.g., "log out everywhere").

**Cons**

- Requires shared state: every module that verifies identity must query the centralized store, introducing a network dependency and a potential bottleneck/single point of failure.
- Directly conflicts with the goal of enabling future extraction into microservices, since every extracted service would remain coupled to a centralized, low-latency-required store.
- Less suitable for cross-boundary or future third-party/service-to-service verification without exposing the store itself.

### Option C: JWT with RS256 (Selected)

**Pros**

- **Asymmetric trust model:** only the authentication module holds the private key; all other modules (and future microservices) only need the public key to verify tokens, without being able to forge them.
- **Stateless verification:** modules can verify a token's authenticity and claims without querying a shared database or session store, reducing coupling and latency.
- **Aligned with Clean Architecture boundaries:** verification becomes an interface (public key / JWKS) that modules depend on, not a shared secret or direct dependency on the authentication module's internals.
- **Smooth path to microservices:** if a module is extracted later, it can keep verifying tokens exactly the same way, since the public key can be published/distributed independently of the private key or the monolith's internal structure.
- **Supports key rotation** without compromising the ability to issue tokens, since only the authentication module manages the private key.

**Cons**

- Higher initial complexity: requires key pair generation, secure storage of the private key, and a mechanism to distribute/rotate the public key (e.g., JWKS endpoint).
- No native revocation: once issued, a token remains valid until expiration unless an additional mechanism (blacklist/allowlist) is introduced, which reintroduces some state.
- Slightly higher computational cost for signing/verification compared to HS256, though this is rarely a bottleneck in practice.
- Requires discipline in implementation (validating `alg`, `aud`, `iss`, rejecting `none` algorithm, etc.) to avoid common JWT-related vulnerabilities.

## Consequences

### Positive

- **Decoupled trust boundaries:** modules can verify identity independently without sharing sensitive signing material, consistent with Clean Architecture's dependency inversion principle.
- **Future-proof for microservices:** authentication verification can be extracted along with any module without redesigning the identity mechanism.
- **Reduced coupling to a centralized store:** most verification is stateless, reducing dependency on shared infrastructure for routine authentication checks.
- **Clear ownership:** only the authentication module can issue tokens, simplifying auditing and reducing the risk of unauthorized token issuance from other modules.

### Negative / Trade-offs

- **Key management overhead:** the team must securely generate, store, rotate, and distribute the RSA key pair (private key protected, public key/JWKS published).
- **No built-in revocation:** additional mechanisms (short expiration times, refresh tokens, or a revocation list) will be needed for cases requiring immediate invalidation (e.g., compromised accounts).
- **Implementation risk:** incorrect validation of JWT claims or algorithms could introduce security vulnerabilities; strict validation practices must be enforced across all verifying modules.

### Items to Monitor

- **Key rotation process:** ensure the RSA key pair can be rotated without downtime and that public key distribution (JWKS) stays consistent across all modules.
- **Revocation strategy:** track whether token expiration alone is sufficient or if a revocation mechanism becomes necessary as the system evolves.
- **Verification consistency:** if modules are extracted into microservices, confirm that each one implements JWT verification correctly and consistently (same validation rules for `alg`, `aud`, `iss`, `exp`).
- **Token payload size:** monitor claim growth (roles, permissions, etc.) to avoid unnecessarily large tokens as the system scales.

## References

- ADR-003: Apply Clean Architecture for each module
- RFC 7519 — JSON Web Token (JWT)
- RFC 7518 — JSON Web Algorithms (JWA)