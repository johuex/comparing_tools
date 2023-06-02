import os

class ConfigHTTP:
    N: int = 10000  # number of total requests
    URL: str = "http://localhost:8000/"
    max_request = os.cpu_count()

class ConfigPostgres:
    host: str = "localhost"
    user: str = "dev_user"
    passwd: str = "123456"
    port: int = 5432
    N: int = 10000
    database: str = "dev_test"
    schema: str = "public"
    table: str = "test"
    max_query: int = os.cpu_count()
    query: str = f"""SELECT * FROM {schema}.{table};"""

config_http = ConfigHTTP()
config_postgres = ConfigPostgres()
