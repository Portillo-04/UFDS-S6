from sqlmodel import Session, select
from config.db import engine
from models.rol import Rol

def seed_roles():
    with Session(engine) as session:
        roles = session.exec(select(Rol)).all()
        nombres = {rol.nombre.lower() for rol in roles}
        if "admin" not in nombres:
            session.add(Rol(nombre="Admin", descripcion="Administrador del sistema"))
        if "vendedor" not in nombres:
            session.add(Rol(nombre="Vendedor", descripcion="Usuario encargado de realizar ventas"))
        session.commit()
