from fastapi_sessions.frontends.implementations import SessionCookie, CookieParameters

cookie_params = CookieParameters()

# Uses UUID
cookie = SessionCookie(
    cookie_name="cookie",
    identifier="general_verifier",
    auto_error=True,
    secret_key="DONOTUSE",
    cookie_params=cookie_params,
)

from uuid import UUID
from fastapi_sessions.backends.implementations import InMemoryBackend
from request_schemas.chat_schemas import SessionData

backend = InMemoryBackend[UUID, SessionData]()