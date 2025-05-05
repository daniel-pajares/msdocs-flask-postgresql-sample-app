from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import validates

from app import db

class ImagenProcesada(db.Model):
    __tablename__ = 'imagen_procesada'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    usuario = Column(String(50))
    fecha = Column(DateTime)
    fases = Column(String(250)) # fases aplicadas, como string separado por comas
    pixeles = Column(JSON) # diccionario de colores y conteo de píxeles

    def __str__(self):
        return f"{self.name} ({self.fecha:%Y-%m-%d %H:%M})"