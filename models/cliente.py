from sqlmodel import SQLModel, Field
from datetime import datetime
from pydantic import EmailStr
from typing import Optional

class ClienteBase(SQLModel):
    nombre: str = Field(nullable=False, max_length=100, min_length=3)
    apellido: str = Field(nullable=False, max_length=100, min_length=3)
    telefono: str = Field(nullable=False, max_length=9, min_length=9)
    correo: Optional[EmailStr] = Field(default=None, max_length=150)
    direccion: Optional[str] = Field(default=None, max_length=255)

class Cliente(ClienteBase, table=True):
    __tablename__ = "clientes"
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime | None = Field(default_factory=datetime.utcnow)
    updated_at: datetime | None = Field(default_factory=datetime.utcnow)

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(ClienteBase):
    pass

class ClienteUpdatePatch(SQLModel):
    nombre: Optional[str] = Field(default=None, max_length=100, min_length=3)
    apellido: Optional[str] = Field(default=None, max_length=100, min_length=3)
    telefono: Optional[str] = Field(default=None, max_length=9, min_length=9)
    correo: Optional[EmailStr] = Field(default=None, max_length=150)
    direccion: Optional[str] = Field(default=None, max_length=255)
