import hashlib
import hmac

import bcrypt


class PasswordHasher:
	"""Password hasher using bcrypt with SHA256 legacy verification fallback."""

	def hash(self, plain_password: str) -> str:
		hashed = bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt())
		return hashed.decode("utf-8")

	def verify(self, plain_password: str, password_hash: str) -> bool:
		if password_hash.startswith("$2"):
			return bcrypt.checkpw(
				plain_password.encode("utf-8"),
				password_hash.encode("utf-8"),
			)

		# Backward compatibility for legacy SHA256 values.
		candidate = hashlib.sha256(plain_password.encode("utf-8")).hexdigest()
		return hmac.compare_digest(candidate, password_hash)

