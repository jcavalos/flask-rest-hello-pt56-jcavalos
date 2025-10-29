import os
from sqlalchemy import create_engine, MetaData
from eralchemy2 import render_er

# Obtener la URL de la base de datos desde las variables de entorno
DATABASE_URL = os.getenv('DATABASE_URL')

if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

if not DATABASE_URL:
    print("Error: DATABASE_URL no está configurada en el archivo .env")
    exit(1)

try:
    # Crear el engine de SQLAlchemy
    engine = create_engine(DATABASE_URL)
    
    # Generar el diagrama usando eralchemy2
    render_er(DATABASE_URL, 'diagram.png')
    
    print("✅ ¡Éxito! El diagrama se ha generado en 'diagram.png'")
    print("📊 Abre el archivo diagram.png para ver tu modelo de datos de Instagram")
    
except Exception as e:
    print(f"❌ Error al generar el diagrama: {e}")
    print("\nIntentando método alternativo...")
    
    try:
        # Método alternativo usando los modelos directamente
        from src.models import db
        from sqlalchemy.orm import declarative_base
        
        Base = declarative_base()
        Base.metadata = db.metadata
        
        render_er(Base, 'diagram.png')
        print("✅ ¡Éxito con el método alternativo! Revisa diagram.png")
        
    except Exception as e2:
        print(f"❌ Error con método alternativo: {e2}")