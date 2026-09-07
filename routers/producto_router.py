from fastapi import APIRouter, HTTPException, status, Query
from sqlmodel import select
from config.session_Dependencia import SessionDeDependencia
from models.categoria import Categoria
from models.producto import Producto, ProductoCreate, ProductoUpdate, ProductoUpdatePatch
from datetime import datetime

router = APIRouter()

@router.get("/productos", response_model=list[Producto], status_code=status.HTTP_200_OK)
def get_productos(session: SessionDeDependencia, offset: int = Query(0, ge=0), limit: int = Query(100, ge=1)):
    return session.exec(select(Producto).offset(offset).limit(limit)).all()

@router.get("/productos/{id}", response_model=Producto, status_code=status.HTTP_200_OK)
def get_producto(id: int, session: SessionDeDependencia):
    producto = session.exec(select(Producto).where(Producto.id == id)).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@router.post('/productos', response_model=Producto, status_code=status.HTTP_201_CREATED)
def create_producto(datos_producto: ProductoCreate, session: SessionDeDependencia):
    categoria = session.exec(select(Categoria).where(Categoria.id == datos_producto.id_categoria)).first()
    if not categoria:
        raise HTTPException(status_code=404, detail=f"Categoria con id {datos_producto.id_categoria} no encontrada")
    producto_nuevo = Producto.model_validate(datos_producto)
    session.add(producto_nuevo)
    session.commit()
    session.refresh(producto_nuevo)
    return producto_nuevo

@router.delete('/productos/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_producto(id: int, session: SessionDeDependencia):
    producto = session.exec(select(Producto).where(Producto.id == id)).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    session.delete(producto)
    session.commit()
    return None

@router.put('/productos/{id}', response_model=Producto, status_code=status.HTTP_200_OK)
def update_producto(id: int, datos_producto: ProductoUpdate, session: SessionDeDependencia):
    producto = session.exec(select(Producto).where(Producto.id == id)).first()
    if not producto:
        raise HTTPException(status_code=404, detail='Producto no encontrado')
    categoria = session.exec(select(Categoria).where(Categoria.id == datos_producto.id_categoria)).first()
    if not categoria:
        raise HTTPException(status_code=404, detail=f"Categoria con id: {datos_producto.id_categoria} no encontrada")
    producto.sqlmodel_update(datos_producto.model_dump())
    producto.updated_at = datetime.utcnow()
    session.add(producto)
    session.commit()
    session.refresh(producto)
    return producto

@router.patch('/productos/{id}', response_model=Producto, status_code=status.HTTP_200_OK)
def patch_producto(id: int, datos_producto: ProductoUpdatePatch, session: SessionDeDependencia):
    producto = session.exec(select(Producto).where(Producto.id == id)).first()
    if not producto:
        raise HTTPException(status_code=404, detail='Producto no encontrado')
    if datos_producto.id_categoria is not None:
        categoria = session.exec(select(Categoria).where(Categoria.id == datos_producto.id_categoria)).first()
        if not categoria:
            raise HTTPException(status_code=404, detail=f"Categoria con id: {datos_producto.id_categoria} no encontrada")
    producto.sqlmodel_update(datos_producto.model_dump(exclude_unset=True))
    producto.updated_at = datetime.utcnow()
    session.add(producto)
    session.commit()
    session.refresh(producto)
    return producto
