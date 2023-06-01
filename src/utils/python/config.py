import os

class ConfigHTTP:
    N: int = 1000  # number of total requests
    URL: str = "https://localhost:8000"  # TODO поменять на какой-нибудь localhost, чтобы не упереться в дудос

class ConfigPostgres:
    host: str = "localhost"
    user: str = "dev_user"
    passwd: str = "123456"
    port: int = 5432
    N: int = 10
    database: str = "dev"
    schema: str = "public"
    table: str = "test"
    max_query: int = os.cpu_count()
    query: str = f"""SELECT * FROM {schema}.{table};"""

config_http = ConfigHTTP()
config_postgres = ConfigPostgres()
