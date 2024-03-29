from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_app_setting
from app.api.routes.api import router as api_router
from app.api.errors.http_error import http_error_handler
from app.api.errors.validation_error import http422_error_handler
from app.db.events import connect_and_init_db, close_db_connection

def get_application() -> FastAPI:
    settings = get_app_setting()

    application = FastAPI(**settings.fastapi_kwargs)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.add_event_handler('startup', connect_and_init_db)
    application.add_event_handler('shutdown', close_db_connection)

    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(RequestValidationError, http422_error_handler)

    application.include_router(api_router, prefix=settings.api_prefix)

    return application

app = get_application()