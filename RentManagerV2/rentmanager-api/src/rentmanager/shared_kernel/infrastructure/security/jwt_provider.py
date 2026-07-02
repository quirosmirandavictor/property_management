from __future__ import annotations

import uuid
from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa


class JwtProvider:
	"""JWT provider that signs tokens with RS256 private keys."""

	def __init__(
		self,
		algorithm: str,
		private_key_pem: str | None,
		public_key_pem: str | None,
		allow_ephemeral_keys: bool = False,
	) -> None:
		self._algorithm = algorithm
		self._private_key_pem = private_key_pem
		self._public_key_pem = public_key_pem

		if self._algorithm != "RS256":
			raise ValueError("Only RS256 is allowed for JWT security.")

		if not self._private_key_pem or not self._public_key_pem:
			if not allow_ephemeral_keys:
				raise ValueError("Missing RSA key material for RS256 provider.")
			self._private_key_pem, self._public_key_pem = self._generate_ephemeral_keys()

	def create_access_token(self, subject: str, user_id: int, expires_minutes: int) -> str:
		now = datetime.now(UTC)
		payload: dict[str, Any] = {
			"sub": subject,
			"uid": user_id,
			"typ": "access",
			"jti": str(uuid.uuid4()),
			"iat": int(now.timestamp()),
			"exp": int((now + timedelta(minutes=expires_minutes)).timestamp()),
		}
		return jwt.encode(payload, self._private_key_pem, algorithm=self._algorithm)

	def create_refresh_token(self, subject: str, expires_days: int) -> str:
		now = datetime.now(UTC)
		payload: dict[str, Any] = {
			"sub": subject,
			"typ": "refresh",
			"jti": str(uuid.uuid4()),
			"iat": int(now.timestamp()),
			"exp": int((now + timedelta(days=expires_days)).timestamp()),
		}
		return jwt.encode(payload, self._private_key_pem, algorithm=self._algorithm)

	def decode_token(self, token: str) -> dict[str, Any]:
		return jwt.decode(token, self._public_key_pem, algorithms=[self._algorithm])

	def _generate_ephemeral_keys(self) -> tuple[str, str]:
		"""Generate temporary RSA keys for local development and tests."""

		private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
		private_pem = private_key.private_bytes(
			encoding=serialization.Encoding.PEM,
			format=serialization.PrivateFormat.PKCS8,
			encryption_algorithm=serialization.NoEncryption(),
		).decode("utf-8")
		public_pem = private_key.public_key().public_bytes(
			encoding=serialization.Encoding.PEM,
			format=serialization.PublicFormat.SubjectPublicKeyInfo,
		).decode("utf-8")
		return private_pem, public_pem

