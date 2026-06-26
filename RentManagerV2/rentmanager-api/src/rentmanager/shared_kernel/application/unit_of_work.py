from abc import ABC, abstractmethod


class UnitOfWork(ABC):
	"""Minimal UoW contract for modular monolith boundaries."""

	@abstractmethod
	def __enter__(self) -> "UnitOfWork":
		raise NotImplementedError

	@abstractmethod
	def __exit__(self, exc_type, exc_val, exc_tb) -> None:
		raise NotImplementedError

	@abstractmethod
	def commit(self) -> None:
		raise NotImplementedError

	@abstractmethod
	def rollback(self) -> None:
		raise NotImplementedError

