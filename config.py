import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'cambiar-esta-clave-en-produccion')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Fix para Postgres en Railway/Render
    uri = os.environ.get('DATABASE_URL', 'sqlite:///psicoagenda.db')
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_DATABASE_URI = uri
