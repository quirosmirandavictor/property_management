from __future__ import annotations


class AssetDomainError(Exception):
	"""Base exception for asset domain and application invariants."""


class AssetNotFoundError(AssetDomainError):
	"""Raised when one asset aggregate cannot be found by identifier."""


class AssetCodeAlreadyExistsError(AssetDomainError):
	"""Raised when attempting to reuse one existing business asset code."""


class InvalidAssetStateError(AssetDomainError):
	"""Raised when one asset payload violates a supported business state."""
