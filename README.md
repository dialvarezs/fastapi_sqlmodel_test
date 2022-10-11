# Cómo inicializar el proyecto

1. Clonar este repositorio
	```bash
	git clone https://github.com/dialvarezs/fastapi_sqlmodel_test
	```
2. Renombrar el archivo `.env.example` a `.env` y modificar el nombre de la base de datos (si es que se quiere utilizar una diferente a la configurada).
3. Eliminar la base de datos si es que ya existe y crearla de nuevo (cambiar el nombre si se utilizó una base de datos diferente en el paso anterior).
	```bash
	dropdb testdb
	createdb testdb
	```
4. Instalar las dependencias (dentro del directorio del repo)
	```bash
	poetry install
	```
5. Activar una terminal dentro del entorno virtual
	```bash
	poetry shell
	```
6. Aplicar las migraciones para crear las tablas
	```bash
	alembic upgrade head
	```
7. Iniciar la aplicación
	```bash
	poe start
	```