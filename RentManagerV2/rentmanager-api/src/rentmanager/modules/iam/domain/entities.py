from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class Functionality:
	"""Domain representation of a platform capability."""

	id: int | None
	code: str
	name: str
	description: str | None = None


@dataclass(slots=True)
class Role:
	"""Domain representation of an authorization role."""

	id: int | None
	name: str
	description: str | None = None
	functionalities: list[Functionality] = field(default_factory=list)


@dataclass(slots=True)
class User:
	"""Domain representation of an authenticated platform user."""

	id: int | None
	dni: str | None
	username: str
	first_name: str
	last_name: str
	email: str
	phone: str | None
	password_hash: str
	is_active: bool = True
	created_at: datetime | None = None
	updated_at: datetime | None = None
	roles: list[Role] = field(default_factory=list)


@dataclass(slots=True)
class RefreshToken:
	"""Domain representation of one persisted refresh token."""

	id: int | None
	user_id: int
	jti: str
	expires_at: datetime
	revoked_at: datetime | None = None
	created_at: datetime | None = None
