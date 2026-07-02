from dataclasses import dataclass


@dataclass(frozen=True)
class AuthenticatedUserDTO:
	"""Authenticated user projection used by API layer."""

	user_id: int
	username: str
