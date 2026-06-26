from datetime import UTC, datetime, timedelta
from typing import Any

import jwt


class JwtProvider:
	def __init__(self, secret_key: str, algorithm: str = "HS256") -> None:
		self._secret_key = secret_key
		self._algorithm = algorithm

	def create_access_token(self, subject: str, expires_minutes: int) -> str:
		now = datetime.now(UTC)
		payload: dict[str, Any] = {
			"sub": subject,
			"iat": int(now.timestamp()),
			"exp": int((now + timedelta(minutes=expires_minutes)).timestamp()),
		}
		return jwt.encode(payload, self._secret_key, algorithm=self._algorithm)

	def decode_token(self, token: str) -> dict[str, Any]:
		return jwt.decode(token, self._secret_key, algorithms=[self._algorithm])

