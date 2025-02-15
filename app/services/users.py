from sqlmodel import Session, select

from app.core.security import get_password_hash
from app.models.core.users import User
from app.schemas.v1.users import UserCreate


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user_create: UserCreate) -> User:
        """Crea un nuevo usuario con su contraseña hasheada."""
        hashed_password = get_password_hash(user_create.password)

        user = User(
            email=user_create.email,
            password_hash=hashed_password,
            first_name=user_create.first_name,
            last_name=user_create.last_name,
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_user_by_email(self, email: str) -> User | None:
        """Obtiene un usuario por su email o devuelve None si no existe."""
        statement = select(User).where(User.email == email)
        return self.db.exec(statement).first()
