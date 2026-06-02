import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.routers import customers, dashboard, health, orders, products

settings = get_settings()

logger = logging.getLogger("uvicorn.error")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan: startup and shutdown events."""
    logger.info("🚀 Starting %s", settings.APP_NAME)
    logger.info("📖 API docs available at /docs")
    logger.info("🔧 Debug mode: %s", settings.DEBUG)
    yield
    logger.info("👋 Shutting down %s", settings.APP_NAME)


app = FastAPI(
    title=settings.APP_NAME,
    description="A production-ready API for managing inventory, customers, and orders.",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    redirect_slashes=False,
)

# ---------------------------------------------------------------------------
# CORS Middleware
# ---------------------------------------------------------------------------
origins = [origin.strip() for origin in settings.ALLOWED_ORIGINS.split(",")]

# CORS spec forbids Access-Control-Allow-Origin: * with credentials.
# When wildcard is used, disable credentials; otherwise reflect the origin.
allow_all = origins == ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=not allow_all,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# CORS-aware error responses
# ---------------------------------------------------------------------------
def _cors_headers(request: Request) -> dict:
    """Build CORS headers matching the middleware config for error responses."""
    origin = request.headers.get("origin", "")
    if allow_all:
        return {
            "access-control-allow-origin": "*",
            "access-control-allow-methods": "*",
            "access-control-allow-headers": "*",
        }
    if origin in origins:
        return {
            "access-control-allow-origin": origin,
            "access-control-allow-credentials": "true",
            "access-control-allow-methods": "*",
            "access-control-allow-headers": "*",
        }
    return {}


def _cors_json(request: Request, status_code: int, content: dict) -> JSONResponse:
    """Return a JSONResponse with CORS headers so browsers don't block errors."""
    return JSONResponse(
        status_code=status_code,
        content=content,
        headers=_cors_headers(request),
    )


# ---------------------------------------------------------------------------
# Global Exception Handlers
# ---------------------------------------------------------------------------
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle HTTP exceptions with a consistent JSON structure."""
    return _cors_json(request, exc.status_code, {"detail": exc.detail})


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Handle request validation errors with details."""
    return _cors_json(
        request,
        status.HTTP_422_UNPROCESSABLE_ENTITY,
        {"detail": "Validation error", "errors": exc.errors()},
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Catch-all handler for unhandled exceptions."""
    logger.exception("Unhandled exception: %s", exc)
    return _cors_json(
        request,
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        {"detail": "Internal server error"},
    )


# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------
app.include_router(health.router)
app.include_router(products.router, prefix=settings.API_V1_PREFIX)
app.include_router(customers.router, prefix=settings.API_V1_PREFIX)
app.include_router(orders.router, prefix=settings.API_V1_PREFIX)
app.include_router(dashboard.router, prefix=settings.API_V1_PREFIX)


# ---------------------------------------------------------------------------
# Root Endpoint
# ---------------------------------------------------------------------------
@app.get("/", tags=["Root"])
async def root() -> dict:
    """Root endpoint with API information."""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "docs_url": "/docs",
    }
