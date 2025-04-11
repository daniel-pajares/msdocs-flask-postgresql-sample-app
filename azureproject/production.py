import os

# Validar que todas las variables de entorno necesarias estén configuradas
required_env_vars = ['AZURE_POSTGRESQL_USER', 'AZURE_POSTGRESQL_PASSWORD', 'AZURE_POSTGRESQL_HOST', 'AZURE_POSTGRESQL_NAME']
missing_vars = [var for var in required_env_vars if not os.getenv(var)]

if missing_vars:
    raise EnvironmentError(f"Faltan las siguientes variables de entorno requeridas: {', '.join(missing_vars)}")

# Construir la URI de la base de datos
DATABASE_URI = 'postgresql+psycopg2://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
    dbuser=os.getenv('AZURE_POSTGRESQL_USER'),
    dbpass=os.getenv('AZURE_POSTGRESQL_PASSWORD'),
    dbhost=os.getenv('AZURE_POSTGRESQL_HOST'),
    dbname=os.getenv('AZURE_POSTGRESQL_NAME')
)