import logging

from fastapi import FastAPI

from app.api import health_check, summaries
from app.db import initialize_database

log = logging.getLogger('uvicorn')


def create_application() -> FastAPI:
    application = FastAPI()
    application.include_router(health_check.router)
    application.include_router(summaries.router, prefix='/summaries', tags=['summaries'])

    return application


app = create_application()


@app.on_event('startup')
async def startup_event():
    log.info('Starting up...')
    initialize_database(app=app)

@app.on_event('shutdown')
async def shutdown_event():
    log.info('Shutting down...')
