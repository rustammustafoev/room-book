from pydantic import BaseSettings, Field

DB_MODELS = ['app.db.models']
DB_URL = "postgres://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"


class PostgresSettings(BaseSettings):
    postgres_user: str = Field(..., env="DB_USER")
    postgres_password: str = Field(..., env="DB_PASSWORD")
    postgres_db: str = Field(..., env="DB_NAME")
    postgres_port: str = Field(..., env="DB_PORT")
    postgres_host: str = Field(..., env="DB_HOST")


class TortoiseSettings(BaseSettings):
    db_url: str
    modules: dict
    generate_schemas: bool

    @classmethod
    def generate(cls):
        postgres = PostgresSettings()
        db_url = DB_URL.format(**postgres.dict())
        del postgres
        modules = {'models': DB_MODELS}

        return TortoiseSettings(db_url=db_url, modules=modules, generate_schemas=True)

    def __repr__(self):
        return f'TortoiseSettings({self.db_url}, {self.modules}, {self.generate_schemas})'
