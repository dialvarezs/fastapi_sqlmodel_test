## Cómo inicializar el proyecto

1. Clonar este repositorio
	```bash
	git clone https://github.com/dialvarezs/fastapi_sqlmodel_test
	```
2. Renombrar el archivo `.env.example` a `.env` y modificar los valores de las variables definidas (si es que se quieren utilizar valores diferentes a los ya anotados).
3. Eliminar la base de datos si es que ya existe y crearla de nuevo (cambiar el nombre si se utilizó una base de datos diferente en el paso anterior).
	```bash
	dropdb testdb
	createdb testdb
	```
4. Instalar las dependencias (dentro del directorio del repo)
	```bash
	poetry install
	```
5. Activar una terminal dentro del entorno virtual (cargando las variables de entorno)
	```bash
	poetry run poe shell
	```
6. Aplicar las migraciones para crear las tablas
	```bash
	alembic upgrade head
	```
7. Iniciar la aplicación
	```bash
	poe start
	```

## Preguntas comunes

### ¿Y si ya tengo el proyecto clonado (pero no tengo la última versión)?
- Ejecutar `git pull` para obtener la última versión.
- Verificar si en `env.example` hay variables nuevas que no estén en `.env`, y si las hay copiarlas y cambiar sus valores si es no quiere utilizarse los valores por defecto.
- Ejecutar los pasos 4 a 7 (por si es que hubieron cambios en las dependencias o en la base de datos).

### En VS Code no funciona el autocompletado, y veo una advertencia que dice "Import `...` could not be resolved from source"

Por defecto, Visual Studio Code utilizará el intérprete del sistema, por lo que el autocompletado no funcionará para las dependencias instaladas a través de Poetry. Entonces, es necesario indicarle a VSCode que utilice el intérprete del entorno virtual, lo cual debe hacerse de la siguiente manera:

1. Buscar la opción `Python: Select Interpreter` (presionar `Ctrl+Shift+P` y empezar a escribir).

2. La opción mostrará una lista, donde debería salir una entrada que tenga la etiqueta "Poetry", seleccionar esa.

3. En caso de que en la lista no salga una entrada con la etiqueta Poetry, se puede ejecutar en el directorio del proyecto
   
   ```bash
   poetry run which python
   ```
   
   El último comando entregará la ruta completa del intérprete, la cual puede pegarse en el campo de texto, en lugar de seleccionar una de las opciones.