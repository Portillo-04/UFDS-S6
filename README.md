# comercial_api

API del sistema comercial desarrollada con FastAPI + SQLModel + MySQL.

## Tablas incluidas

- roles
- usuarios
- categorias
- productos
- clientes
- ventas
- detalle_ventas
- tipo_pago

## CRUD

Todas las tablas tienen endpoints para consultar, crear, actualizar y eliminar registros. Los recursos que lo necesitan también validan sus claves foráneas.

## Requisito de la tarea

Al iniciar la aplicación se crean las tablas y se agregan automáticamente los roles `Admin` y `Vendedor` si todavía no existen.

El `username` de usuarios es único tanto al crear como al actualizar.

## Configuración

1. Copiar `.ven-ejemplo` como `.env`.
2. Crear la base de datos MySQL `comercial`.
3. Ajustar usuario, contraseña, host y puerto en `.env`.
4. Instalar dependencias:

```bash
pip install -r requirements.txt
```

5. Ejecutar:

```bash
uvicorn main:app --reload
```

6. Abrir Swagger en `http://127.0.0.1:8000/docs`.

## Endpoints principales

- `/roles`
- `/usuarios`
- `/categorias`
- `/productos`
- `/clientes`
- `/ventas`
- `/detalle-ventas`
- `/tipos-pago`
- `/oauth/login`
