# Pokémon App con Django y SQL Server

Una aplicación web que permite gestionar tu colección personal de Pokémon utilizando la PokeAPI.

## Características Principales

- Sistema de autenticación de usuarios
- Integración con PokeAPI
- Gestión de colección de Pokémon
- Filtros y ordenamiento avanzado
- Paginación de resultados
- Vistas en tarjetas y lista
- Diseño responsive con Bootstrap 5

## Requisitos del Sistema

- Python 3.12+
- SQL Server (Aca Utilice 2022) https://go.microsoft.com/fwlink/p/?linkid=2216019&clcid=0x340a&culture=es-cl&country=cl
- ODBC Driver 17 for SQL Server https://go.microsoft.com/fwlink/?linkid=2266337
- pip (gestor de paquetes de Python)
- Entorno virtual de Python (venv)

## Instalación de comandos en la terminal

1. Clonar el repositorio:
```bash
git clone https://github.com/C1ZC/web_proyect.git

```
2. Ingregar a la carpeta el repositorio:
```bash
cd .\web_project\

```

3. Configurar entorno virtual:
```bash
python -m venv .venv
.venv\Scripts\activate
```

4. Instalar updates:
```bash
python.exe -m pip install --upgrade pip
```

5. Instalar dependencias:
```bash
pip install -r requirements.txt
```


## Configuración

1. Crear la base de datos en SQL Server:
   
   Abre SQL Server Management Studio (SSMS) y ejecuta:
```sql
CREATE DATABASE web_app;
GO
```
   O desde la línea de comandos:
```bash
sqlcmd -S localhost -U sa -P tu-contraseña -Q "CREATE DATABASE web_app"
```

2. Configurar variables de entorno - crear archivo `.env`:
```env
# Django
DJANGO_SECRET_KEY=tu-clave-secreta
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,tudominio.com

# SQL Server
DB_ENGINE=mssql
DB_NAME=web_app
DB_USER=sa
DB_PASSWORD=tu-contraseña
DB_HOST=localhost
DB_PORT=1433
DB_DRIVER=ODBC Driver 17 for SQL Server
DB_ENCRYPTION=no
```

3. Verificar la conexión a la base de datos:
```bash
python manage.py dbshell
```
Si la conexión es exitosa, verás el prompt de SQL Server.

4. Aplicar migraciones:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Crear superusuario:
```bash
python manage.py createsuperuser
```

username: admin
email: admin@mail.com
pass: admin123


6. Compilar estáticos:
```bash
python manage.py collectstatic
```

## Uso

1. Iniciar el servidor:
```bash
python manage.py runserver
```

2. Acceder a:
- Aplicación: http://127.0.0.1:8000
- Administración: http://127.0.0.1:8000/admin


## Estructura

```
web_project/
├── web_app/
│   ├── static/          # Archivos estáticos
│   ├── templates/       # Plantillas HTML
│   ├── services/        # Servicios y lógica de negocio
│   ├── models.py        # Modelos de datos
│   └── views.py         # Vistas y controladores
├── .env                 # Variables de entorno
├── manage.py
└── requirements.txt     # Dependencias
```

## Tecnologías

- Django 5.0.14
- SQL Server
- Bootstrap 5
- PokeAPI
- JavaScript

## Variables de Entorno

| Variable | Descripción |
|----------|-------------|
| DJANGO_SECRET_KEY | Clave secreta de Django |
| DB_ENGINE | Motor de base de datos (mssql) |
| DB_NAME | Nombre de base de datos |
| DB_USER | Usuario SQL Server |
| DB_PASSWORD | Contraseña |
| DB_HOST | Host del servidor |
| DB_PORT | Puerto (default 1433) |
| DB_DRIVER | Driver ODBC |

## Contribuir

1. Fork el proyecto desde https://github.com/C1ZC/web_proyect
2. Crear rama de característica (`git checkout -b feature/nueva-caracteristica`)
3. Commit cambios (`git commit -m 'Agrega nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Crear Pull Request en https://github.com/C1ZC/web_proyect/pulls

## Autor

Camilo Zavala Cornejo
- GitHub: [C1ZC](https://github.com/C1ZC)

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.