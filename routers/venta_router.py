from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Query
from sqlmodel import select
from config.session_Dependencia import SessionDeDependencia
from models.venta import Venta, VentaCreate, VentaUpdate
from models.cliente import Cliente
from models.usuario import Usuario
from models.tipo_pago import TipoPago

router = APIRouter()

def validar_referencias(datos, session):
    if not session.get(Cliente, datos.id_cliente):
        raise HTTPException(status_code=404, detail=f"Cliente con id {datos.id_cliente} no encontrado")
    if not session.get(Usuario, datos.id_usuario):
        raise HTTPException(status_code=404, detail=f"Usuario con id {datos.id_usuario} no encontrado")
    if not session.get(TipoPago, datos.id_tipo_pago):
        raise HTTPException(status_code=404, detail=f"Tipo de pago con id {datos.id_tipo_pago} no encontrado")

@router.get("/ventas", response_model=list[Venta], status_code=status.HTTP_200_OK)
def get_ventas(session: SessionDeDependencia, offset: int = Query(0, ge=0), limit: int = Query(100, ge=1)):
    return session.exec(select(Venta).offset(offset).limit(limit)).all()

@router.get("/ventas/{id}", response_model=Venta, status_code=status.HTTP_200_OK)
def get_venta(id: int, session: SessionDeDependencia):
    venta = session.get(Venta, id)
    if not venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    return venta

@router.post("/ventas", response_model=Venta, status_code=status.HTTP_201_CREATED)
def create_venta(datos: VentaCreate, session: SessionDeDependencia):
    validar_referencias(datos, session)
    venta = Venta.model_validate(datos)
    session.add(venta)
    session.commit()
    session.refresh(venta)
    return venta

@router.delete("/ventas/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_venta(id: int, session: SessionDeDependencia):
    venta = session.get(Venta, id)
    if not venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    session.delete(venta)
    session.commit()
    return None

@router.put("/ventas/{id}", response_model=Venta, status_code=status.HTTP_200_OK)
def update_venta(id: int, datos: VentaUpdate, session: SessionDeDependencia):
    venta = session.get(Venta, id)
    if not venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    validar_referencias(datos, session)
    venta.sqlmodel_update(datos.model_dump())
    venta.updated_at = datetime.utcnow()
    session.add(venta)
    session.commit()
    session.refresh(venta)
    return venta
