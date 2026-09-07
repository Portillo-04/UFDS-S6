from fastapi import APIRouter, HTTPException, status, Query
from sqlmodel import select
from config.session_Dependencia import SessionDeDependencia
from models.rol import Rol
from models.usuario import Usuario, UsuarioCreate, UsuarioUpdate, UsuarioUpdatePatch
from datetime import datetime
from lib.pwd import get_password_hash

router = APIRouter()

@router.get("/usuarios", response_model=list[Usuario], status_code=status.HTTP_200_OK)
async def get_usuarios(session: SessionDeDependencia, offset: int = Query(0, ge=0), limit: int = Query(100, ge=1)):
    return session.exec(select(Usuario).offset(offset).limit(limit)).all()

@router.get("/usuarios/{id}", response_model=Usuario, status_code=status.HTTP_200_OK)
async def get_usuario(id: int, session: SessionDeDependencia):
    usuario = session.exec(select(Usuario).where(Usuario.id == id)).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.post('/usuarios', response_model=Usuario, status_code=status.HTTP_201_CREATED)
async def create_usuario(datos_usuario: UsuarioCreate, session: SessionDeDependencia):
    if session.exec(select(Usuario).where(Usuario.username == datos_usuario.username)).first():
        raise HTTPException(status_code=400, detail="El nombre de usuario ya está en uso")
    if not session.get(Rol, datos_usuario.id_rol):
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    usuario_nuevo = Usuario(
        username=datos_usuario.username,
        password=get_password_hash(datos_usuario.password),
        nombre=datos_usuario.nombre,
        apellido=datos_usuario.apellido,
        telefono=datos_usuario.telefono,
        correo=datos_usuario.correo,
        id_rol=datos_usuario.id_rol,
    )
    session.add(usuario_nuevo)
    session.commit()
    session.refresh(usuario_nuevo)
    return usuario_nuevo

@router.delete('/usuarios/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_usuario(id: int, session: SessionDeDependencia):
    usuario = session.exec(select(Usuario).where(Usuario.id == id)).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    session.delete(usuario)
    session.commit()
    return None

@router.put('/usuarios/{id}', response_model=Usuario, status_code=status.HTTP_200_OK)
async def update_usuario(id: int, datos_usuario: UsuarioUpdate, session: SessionDeDependencia):
    usuario = session.exec(select(Usuario).where(Usuario.id == id)).first()
    if not usuario:
        raise HTTPException(status_code=404, detail='Usuario no encontrado')
    existente = session.exec(select(Usuario).where(Usuario.username == datos_usuario.username, Usuario.id != id)).first()
    if existente:
        raise HTTPException(status_code=400, detail="El nombre de usuario ya está en uso")
    if not session.get(Rol, datos_usuario.id_rol):
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    usuario.username = datos_usuario.username
    usuario.password = get_password_hash(datos_usuario.password)
    usuario.nombre = datos_usuario.nombre
    usuario.apellido = datos_usuario.apellido
    usuario.telefono = datos_usuario.telefono
    usuario.correo = datos_usuario.correo
    usuario.id_rol = datos_usuario.id_rol
    usuario.updated_at = datetime.utcnow()
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario

@router.patch('/usuarios/{id}', response_model=Usuario, status_code=status.HTTP_200_OK)
async def patch_usuario(id: int, datos_usuario: UsuarioUpdatePatch, session: SessionDeDependencia):
    usuario = session.exec(select(Usuario).where(Usuario.id == id)).first()
    if not usuario:
        raise HTTPException(status_code=404, detail='Usuario no encontrado')
    cambios = datos_usuario.model_dump(exclude_unset=True)
    if 'username' in cambios:
        existente = session.exec(select(Usuario).where(Usuario.username == cambios['username'], Usuario.id != id)).first()
        if existente:
            raise HTTPException(status_code=400, detail="El nombre de usuario ya está en uso")
    if 'id_rol' in cambios and cambios['id_rol'] is not None and not session.get(Rol, cambios['id_rol']):
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    if 'password' in cambios and cambios['password']:
        cambios['password'] = get_password_hash(cambios['password'])
    usuario.sqlmodel_update(cambios)
    usuario.updated_at = datetime.utcnow()
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario
