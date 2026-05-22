import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'cambiar-esta-clave-en-produccion')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Fix para Postgres en Railway/Render/Azure
    default_db = 'sqlite:///' + os.path.join(BASE_DIR, 'instance', 'psicoagenda.db')
    uri = os.environ.get('DATABASE_URL', default_db)
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_DATABASE_URI = uri
