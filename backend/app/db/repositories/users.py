from datetime import datetime
from typing import Optional
from .base import BaseRepository
from ...models.user import UserInDB, UserCreate
from ...core.security import get_password_hash

class UsersRepository(BaseRepository[UserInDB]):
    async def get_by_email(self, email: str) -> Optional[UserInDB]:
        return await self.find_one({"email": email})

    async def create_user(self, user: UserCreate) -> UserInDB:
        user_data = user.model_dump()
        user_data.update({
            "hashed_password": get_password_hash(user_data.pop("password")),
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        })
        return await self.create(user_data)