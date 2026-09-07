from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Query
from models.rol import Rol, RolCreate, RolUpdate
from sqlmodel import select
from config.session_Dependencia import SessionDeDependencia

router = APIRouter()

@router.get("/roles", response_model=list[Rol], status_code=status.HTTP_200_OK)
def get_roles(session: SessionDeDependencia, offset: int = Query(0, ge=0), limit: int = Query(20, ge=1)):
    return session.exec(select(Rol).offset(offset).limit(limit)).all()

@router.get("/roles/{id}", response_model=Rol, status_code=status.HTTP_200_OK)
def get_rol(id: int, session: SessionDeDependencia):
    rol = session.exec(select(Rol).where(Rol.id == id)).first()
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return rol

@router.post("/roles", response_model=Rol, status_code=status.HTTP_201_CREATED)
def create_rol(datos_rol: RolCreate, session: SessionDeDependencia):
    rol_nuevo = Rol(nombre=datos_rol.nombre, descripcion=datos_rol.descripcion)
    session.add(rol_nuevo)
    session.commit()
    session.refresh(rol_nuevo)
    return rol_nuevo

@router.delete("/roles/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_rol(id: int, session: SessionDeDependencia):
    rol = session.exec(select(Rol).where(Rol.id == id)).first()
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    session.delete(rol)
    session.commit()
    return None

@router.put("/roles/{id}", response_model=Rol, status_code=status.HTTP_200_OK)
def update_rol(id: int, datos_rol: RolUpdate, session: SessionDeDependencia):
    rol = session.exec(select(Rol).where(Rol.id == id)).first()
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    rol.nombre = datos_rol.nombre
    rol.descripcion = datos_rol.descripcion
    rol.updated_at = datetime.utcnow()
    session.add(rol)
    session.commit()
    session.refresh(rol)
    return rol
