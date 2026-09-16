import hashlib
import secrets


def generate_session_token() -> str:
	return secrets.token_urlsafe(32)


def hash_session_token(session_token: str) -> str:
	return hashlib.sha256(session_token.encode("utf-8")).hexdigest()


def verify_session_token(session_token: str, session_token_hash: str) -> bool:
	return secrets.compare_digest(
		hash_session_token(session_token),
		session_token_hash,
	)