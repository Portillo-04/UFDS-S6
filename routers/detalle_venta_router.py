from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Query
from sqlmodel import select
from config.session_Dependencia import SessionDeDependencia
from models.detalle_venta import DetalleVenta, DetalleVentaCreate, DetalleVentaUpdate
from models.venta import Venta
from models.producto import Producto

router = APIRouter()

def validar_referencias(datos, session):
    if not session.get(Venta, datos.id_venta):
        raise HTTPException(status_code=404, detail=f"Venta con id {datos.id_venta} no encontrada")
    if not session.get(Producto, datos.id_producto):
        raise HTTPException(status_code=404, detail=f"Producto con id {datos.id_producto} no encontrado")

@router.get("/detalle-ventas", response_model=list[DetalleVenta], status_code=status.HTTP_200_OK)
def get_detalles(session: SessionDeDependencia, offset: int = Query(0, ge=0), limit: int = Query(100, ge=1)):
    return session.exec(select(DetalleVenta).offset(offset).limit(limit)).all()

@router.get("/detalle-ventas/{id}", response_model=DetalleVenta, status_code=status.HTTP_200_OK)
def get_detalle(id: int, session: SessionDeDependencia):
    detalle = session.get(DetalleVenta, id)
    if not detalle:
        raise HTTPException(status_code=404, detail="Detalle de venta no encontrado")
    return detalle

@router.post("/detalle-ventas", response_model=DetalleVenta, status_code=status.HTTP_201_CREATED)
def create_detalle(datos: DetalleVentaCreate, session: SessionDeDependencia):
    validar_referencias(datos, session)
    detalle = DetalleVenta.model_validate(datos)
    session.add(detalle)
    session.commit()
    session.refresh(detalle)
    return detalle

@router.delete("/detalle-ventas/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_detalle(id: int, session: SessionDeDependencia):
    detalle = session.get(DetalleVenta, id)
    if not detalle:
        raise HTTPException(status_code=404, detail="Detalle de venta no encontrado")
    session.delete(detalle)
    session.commit()
    return None

@router.put("/detalle-ventas/{id}", response_model=DetalleVenta, status_code=status.HTTP_200_OK)
def update_detalle(id: int, datos: DetalleVentaUpdate, session: SessionDeDependencia):
    detalle = session.get(DetalleVenta, id)
    if not detalle:
        raise HTTPException(status_code=404, detail="Detalle de venta no encontrado")
    validar_referencias(datos, session)
    detalle.sqlmodel_update(datos.model_dump())
    detalle.updated_at = datetime.utcnow()
    session.add(detalle)
    session.commit()
    session.refresh(detalle)
    return detalle
