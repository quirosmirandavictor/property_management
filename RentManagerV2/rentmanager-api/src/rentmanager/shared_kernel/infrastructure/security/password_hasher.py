import hashlib
import hmac


class PasswordHasher:
	def hash(self, plain_password: str) -> str:
		return hashlib.sha256(plain_password.encode("utf-8")).hexdigest()

	def verify(self, plain_password: str, password_hash: str) -> bool:
		candidate = self.hash(plain_password)
		return hmac.compare_digest(candidate, password_hash)

