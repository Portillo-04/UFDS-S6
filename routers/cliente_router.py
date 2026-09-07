from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Query
from sqlmodel import select
from config.session_Dependencia import SessionDeDependencia
from models.cliente import Cliente, ClienteCreate, ClienteUpdate, ClienteUpdatePatch

router = APIRouter()

@router.get("/clientes", response_model=list[Cliente], status_code=status.HTTP_200_OK)
def get_clientes(session: SessionDeDependencia, offset: int = Query(0, ge=0), limit: int = Query(100, ge=1)):
    return session.exec(select(Cliente).offset(offset).limit(limit)).all()

@router.get("/clientes/{id}", response_model=Cliente, status_code=status.HTTP_200_OK)
def get_cliente(id: int, session: SessionDeDependencia):
    cliente = session.exec(select(Cliente).where(Cliente.id == id)).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

@router.post("/clientes", response_model=Cliente, status_code=status.HTTP_201_CREATED)
def create_cliente(datos: ClienteCreate, session: SessionDeDependencia):
    cliente = Cliente.model_validate(datos)
    session.add(cliente)
    session.commit()
    session.refresh(cliente)
    return cliente

@router.delete("/clientes/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cliente(id: int, session: SessionDeDependencia):
    cliente = session.exec(select(Cliente).where(Cliente.id == id)).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    session.delete(cliente)
    session.commit()
    return None

@router.put("/clientes/{id}", response_model=Cliente, status_code=status.HTTP_200_OK)
def update_cliente(id: int, datos: ClienteUpdate, session: SessionDeDependencia):
    cliente = session.exec(select(Cliente).where(Cliente.id == id)).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    cliente.sqlmodel_update(datos.model_dump())
    cliente.updated_at = datetime.utcnow()
    session.add(cliente)
    session.commit()
    session.refresh(cliente)
    return cliente

@router.patch("/clientes/{id}", response_model=Cliente, status_code=status.HTTP_200_OK)
def patch_cliente(id: int, datos: ClienteUpdatePatch, session: SessionDeDependencia):
    cliente = session.exec(select(Cliente).where(Cliente.id == id)).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    cliente.sqlmodel_update(datos.model_dump(exclude_unset=True))
    cliente.updated_at = datetime.utcnow()
    session.add(cliente)
    session.commit()
    session.refresh(cliente)
    return cliente
