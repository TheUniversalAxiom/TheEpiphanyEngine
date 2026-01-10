"""
Security middleware for Epiphany Engine API.

Implements security headers and CORS best practices.
"""

import os
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware to add security headers to all responses.

    Headers added:
    - X-Content-Type-Options: Prevent MIME type sniffing
    - X-Frame-Options: Prevent clickjacking
    - X-XSS-Protection: Enable XSS filtering (legacy browsers)
    - Strict-Transport-Security: Enforce HTTPS (production only)
    - Content-Security-Policy: Restrict resource loading
    - Referrer-Policy: Control referrer information
    - Permissions-Policy: Control browser features
    """

    def __init__(self, app, enable_hsts: bool = False):
        """
        Initialize security headers middleware.

        Args:
            app: FastAPI application
            enable_hsts: Enable HSTS header (only in production with HTTPS)
        """
        super().__init__(app)
        self.enable_hsts = enable_hsts

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Add security headers to response."""
        response = await call_next(request)

        # Prevent MIME type sniffing
        response.headers["X-Content-Type-Options"] = "nosniff"

        # Prevent clickjacking
        response.headers["X-Frame-Options"] = "DENY"

        # Enable XSS filtering (legacy browsers)
        response.headers["X-XSS-Protection"] = "1; mode=block"

        # Content Security Policy
        # Allow resources only from same origin, inline styles for docs
        csp_directives = [
            "default-src 'self'",
            "script-src 'self' 'unsafe-inline'",  # unsafe-inline needed for Swagger UI
            "style-src 'self' 'unsafe-inline'",   # unsafe-inline needed for Swagger UI
            "img-src 'self' data:",                # data: for Swagger UI logos
            "font-src 'self'",
            "connect-src 'self'",
            "frame-ancestors 'none'",              # Equivalent to X-Frame-Options
            "base-uri 'self'",
            "form-action 'self'",
        ]
        response.headers["Content-Security-Policy"] = "; ".join(csp_directives)

        # Referrer Policy - only send referrer for same-origin requests
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # Permissions Policy - disable unnecessary browser features
        permissions_directives = [
            "geolocation=()",
            "microphone=()",
            "camera=()",
            "payment=()",
            "usb=()",
            "magnetometer=()",
            "gyroscope=()",
            "accelerometer=()",
        ]
        response.headers["Permissions-Policy"] = ", ".join(permissions_directives)

        # HSTS - only enable in production with HTTPS
        if self.enable_hsts:
            # max-age=31536000 = 1 year
            response.headers["Strict-Transport-Security"] = (
                "max-age=31536000; includeSubDomains; preload"
            )

        return response


def get_hsts_enabled() -> bool:
    """
    Check if HSTS should be enabled based on environment.

    HSTS should only be enabled when:
    1. In production environment
    2. Using HTTPS (behind reverse proxy)

    Returns:
        True if HSTS should be enabled
    """
    env = os.getenv("ENVIRONMENT", "development").lower()
    https_enabled = os.getenv("HTTPS_ENABLED", "false").lower() == "true"

    return env == "production" and https_enabled
