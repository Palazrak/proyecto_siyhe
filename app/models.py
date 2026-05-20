from sqlalchemy import Column, Integer, String, Sequence

from .database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(
        Integer,
        Sequence("usuarios_id_usuario_seq", start=0, minvalue=0, increment=1),
        primary_key=True,
        nullable=False,
    )
    usuario = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    placa = Column(String(20), nullable=True)
