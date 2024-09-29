
import time
from typing import Optional

from api.configs import dify_config
from api.extensions.ext_redis import redis_client
from api.libs.helper import generate_string, generate_text_hash
from api.services.errors.account import RateLimitExceededError


class VerificationService:
    @classmethod
    def generate_account_deletion_verification_code(cls, email: str) -> str:
        return cls._generate_verification_code(
            email=email,
            prefix="account_deletion",
            expire=dify_config.VERIFICATION_CODE_EXPIRY,
            code_length=dify_config.VERIFICATION_CODE_LENGTH
        )

    @classmethod
    def verify_account_deletion_verification_code(cls, email: str, verification_code: str) -> bool:
        return cls._verify_verification_code(
            email=email,
            prefix="account_deletion",
            verification_code=verification_code
        )

    ### Helper methods ###

    @classmethod
    def _generate_verification_code(cls, key_name: str, prefix: str, expire: int = 300, code_length: int = 6) -> str:
        hashed_key = generate_text_hash(key_name)
        key, time_key = cls._get_key(f"{prefix}:{hashed_key}")
        now = int(time.time())

        # Check if there is already a verification code for this key within 1 minute
        created_at = redis_client.get(time_key)
        if created_at is not None and now - created_at < dify_config.VERIFICATION_CODE_COOLDOWN:
            raise RateLimitExceededError()

        created_at = now
        verification_code = generate_string(code_length)

        redis_client.setex(key, expire, verification_code)
        redis_client.setex(time_key, expire, created_at)
        return verification_code

    @classmethod
    def _get_verification_code(cls, prefix: str, key_name: str) -> Optional[str]:
        hashed_key = generate_text_hash(key_name)
        key, _ = cls._get_key(f"{prefix}:{hashed_key}")
        verification_code = redis_client.get(key)

        return verification_code

    @classmethod
    def _verify_verification_code(cls, key_name: str, prefix: str, verification_code: str) -> bool:
        hashed_key = generate_text_hash(key_name)
        key, _ = cls._get_key(f"{prefix}:{hashed_key}")
        stored_verification_code = redis_client.get(key)

        if stored_verification_code is None:
            return False
        return stored_verification_code == verification_code

    @classmethod
    def _get_key(cls, key_name: str) -> str:
        return f"verification:{key_name}", f"verification:{key_name}:time"
