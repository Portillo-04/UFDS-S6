from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Query
from models.categoria import Categoria, CategoriaCreate, CategoriaUpdate
from sqlmodel import select
from config.session_Dependencia import SessionDeDependencia
from config.segurity_Dependencia import Token_Dependencia

router = APIRouter()

@router.get("/categorias", response_model=list[Categoria], status_code=status.HTTP_200_OK)
async def get_categorias(session: SessionDeDependencia, token: Token_Dependencia,
                         offset: int = Query(0, ge=0), limit: int = Query(20, ge=1)):
    if token['id_rol'] != 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="No tienes permisos para acceder a esta información")
    consulta = select(Categoria).offset(offset).limit(limit)
    return session.exec(consulta).all()

@router.get("/categorias/{id}", response_model=Categoria, status_code=status.HTTP_200_OK)
async def get_categoria(id: int, session: SessionDeDependencia):
    categoria = session.exec(select(Categoria).where(Categoria.id == id)).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")
    return categoria

@router.post("/categorias", response_model=Categoria, status_code=status.HTTP_201_CREATED)
async def create_categoria(datos_categoria: CategoriaCreate, session: SessionDeDependencia):
    categoria_nueva = Categoria(nombre=datos_categoria.nombre, descripcion=datos_categoria.descripcion)
    session.add(categoria_nueva)
    session.commit()
    session.refresh(categoria_nueva)
    return categoria_nueva

@router.delete("/categorias/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_categoria(id: int, session: SessionDeDependencia):
    categoria = session.exec(select(Categoria).where(Categoria.id == id)).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")
    session.delete(categoria)
    session.commit()
    return None

@router.put("/categorias/{id}", response_model=Categoria, status_code=status.HTTP_200_OK)
async def update_categoria(id: int, datos_categoria: CategoriaUpdate, session: SessionDeDependencia):
    categoria = session.exec(select(Categoria).where(Categoria.id == id)).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")
    categoria.nombre = datos_categoria.nombre
    categoria.descripcion = datos_categoria.descripcion
    categoria.updated_at = datetime.utcnow()
    session.add(categoria)
    session.commit()
    session.refresh(categoria)
    return categoria
