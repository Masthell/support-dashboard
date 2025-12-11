from sqlalchemy.ext.declarative import declarative_base

# Единый источник достоверной информации для Base
Base = declarative_base()

from .user import User

__all__ = ["Base", "User"]