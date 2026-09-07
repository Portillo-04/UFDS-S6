from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Query
from sqlmodel import select
from config.session_Dependencia import SessionDeDependencia
from models.tipo_pago import TipoPago, TipoPagoCreate, TipoPagoUpdate

router = APIRouter()

@router.get("/tipos-pago", response_model=list[TipoPago], status_code=status.HTTP_200_OK)
def get_tipos_pago(session: SessionDeDependencia, offset: int = Query(0, ge=0), limit: int = Query(100, ge=1)):
    return session.exec(select(TipoPago).offset(offset).limit(limit)).all()

@router.get("/tipos-pago/{id}", response_model=TipoPago, status_code=status.HTTP_200_OK)
def get_tipo_pago(id: int, session: SessionDeDependencia):
    item = session.exec(select(TipoPago).where(TipoPago.id == id)).first()
    if not item:
        raise HTTPException(status_code=404, detail="Tipo de pago no encontrado")
    return item

@router.post("/tipos-pago", response_model=TipoPago, status_code=status.HTTP_201_CREATED)
def create_tipo_pago(datos: TipoPagoCreate, session: SessionDeDependencia):
    item = TipoPago.model_validate(datos)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item

@router.delete("/tipos-pago/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tipo_pago(id: int, session: SessionDeDependencia):
    item = session.exec(select(TipoPago).where(TipoPago.id == id)).first()
    if not item:
        raise HTTPException(status_code=404, detail="Tipo de pago no encontrado")
    session.delete(item)
    session.commit()
    return None

@router.put("/tipos-pago/{id}", response_model=TipoPago, status_code=status.HTTP_200_OK)
def update_tipo_pago(id: int, datos: TipoPagoUpdate, session: SessionDeDependencia):
    item = session.exec(select(TipoPago).where(TipoPago.id == id)).first()
    if not item:
        raise HTTPException(status_code=404, detail="Tipo de pago no encontrado")
    item.sqlmodel_update(datos.model_dump())
    item.updated_at = datetime.utcnow()
    session.add(item)
    session.commit()
    session.refresh(item)
    return item
