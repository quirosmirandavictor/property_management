class InvalidCredentialsError(ValueError):
	"""Raised when submitted credentials are invalid."""


class UserInactiveError(ValueError):
	"""Raised when an inactive user tries to authenticate."""


class InvalidRefreshTokenError(ValueError):
	"""Raised when the refresh token is malformed, missing, or revoked."""
