from __init__ import (
    FI_DEBUG,
    FI_JWT_SECRET,
    FI_JWT_SECRET_API
)

DEBUG = FI_DEBUG == 'True'

TIME_ZONE = 'America/Bogota'

# JWT
JWT_COOKIE_NAME = "integrates_session"
JWT_COOKIE_SAMESITE = "Lax"
JWT_SECRET = FI_JWT_SECRET
JWT_SECRET_API = FI_JWT_SECRET_API

# Session
SESSION_COOKIE_AGE = 40 * 60

# Cache
CACHE_TTL = 60 * 60 * 8
