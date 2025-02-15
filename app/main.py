import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.router import api_router
from app.core.config import settings
from app.database.session import create_db_and_tables, engine
from app.utils.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manejo del ciclo de vida de la aplicación"""
    # Startup
    logger.info("Starting application...")

    if settings.ENVIRONMENT == "development":
        logger.debug("Creating database tables")
        create_db_and_tables()

    yield

    # Shutdown
    logger.info("Shutting down application...")
    if engine:
        await engine.dispose()


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="API para gestión de suscripciones y servicios relacionados",
    lifespan=lifespan,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    contact={"name": "Soporte Técnico", "email": "soporte@miservicio.com"},
    license_info={
        "name": "MIT",
    },
)

# Middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)


# Middleware de logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000

    logger.info(
        "Request processed",
        extra={
            "path": request.url.path,
            "method": request.method,
            "status": response.status_code,
            "process_time": f"{process_time:.2f}ms",
        },
    )

    return response


# Manejador de errores global
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(
        "Unhandled exception occurred",
        exc_info=exc,
        extra={"path": request.url.path, "method": request.method},
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal Server Error"},
    )


# Incluir rutas principales
app.include_router(api_router, prefix=settings.API_V1_STR, tags=["v1"])


# Health Check Endpoint
@app.get("/health", summary="Verificar estado del servicio", tags=["System"])
async def health_check():
    return {
        "status": "OK",
        "environment": settings.ENVIRONMENT,
        "debug": settings.DEBUG,
        "database": "connected" if engine else "disconnected",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_config=None,
        log_level="debug" if settings.DEBUG else "info",
        server_header=False,
    )
