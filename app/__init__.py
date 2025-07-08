# app/__init__.py
from .main import app
from . import models, schemas, database, auth

# Optional: Initialize database models
def init_db():
    models.Base.metadata.create_all(bind=database.engine)

__all__ = ["app", "models", "schemas", "database", "auth", "init_db"]