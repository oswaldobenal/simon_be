from pydantic import Field, PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Configuración de la aplicación
    APP_NAME: str = "Simon Services"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    API_V1_STR: str = "/api/v1"

    # Configuración de base de datos
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str
    POSTGRES_TEST_DB: str = "test_db"

    # Seguridad
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=10080,  # 7 días en minutos
        description="Tiempo de expiración del token JWT en minutos",
    )
    ALGORITHM: str = "HS256"

    # CORS
    CORS_ORIGINS: list[str] = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list[str] = ["*"]
    CORS_ALLOW_HEADERS: list[str] = ["*"]

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=int(self.POSTGRES_PORT),
            path=self.POSTGRES_DB,
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
        env_prefix="SIMON_",  # Opcional: prefijo para variables de entorno
        validate_default=True,
    )


settings = Settings()
