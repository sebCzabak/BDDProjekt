# backend/alembic/env.py
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# --- DODAJ TE IMPORTY ---
from app.database import Base
from app.models import CurrencyRate # Ważne, aby modele były zaimportowane
# ------------------------