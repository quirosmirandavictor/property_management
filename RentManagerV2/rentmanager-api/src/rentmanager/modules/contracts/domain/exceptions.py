from __future__ import annotations


class ContractDomainError(Exception):
	"""Base exception for contract domain and application invariants."""


class ContractNotFoundError(ContractDomainError):
	"""Raised when one contract aggregate cannot be found by identifier."""


class ContractCodeAlreadyExistsError(ContractDomainError):
	"""Raised when attempting to reuse one existing contract business code."""


class InvalidContractStateError(ContractDomainError):
	"""Raised when one contract payload violates a supported business state."""


class ContractTenantAlreadyAssignedError(ContractDomainError):
	"""Raised when trying to add one tenant that is already linked to a contract."""


class ContractTenantNotFoundError(ContractDomainError):
	"""Raised when trying to remove one tenant that is not linked to a contract."""
