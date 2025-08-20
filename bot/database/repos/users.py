from __future__ import annotations

from typing import Sequence

from sqlalchemy import INTEGER, Float, select, desc
from sqlalchemy.orm import selectinload, InstrumentedAttribute

from .base import BaseRepo
from bot.database.models import User


class UsersRepo(BaseRepo):
    model = User

    async def update_user_field(self, user_id: int, **fields):
        user = await self.get_by_user_id(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
        
        # Get the model's column types
        mapper = User.__mapper__
        
        for field, value in fields.items():
            if value is None:
                setattr(user, field, None)
                continue
                
            # Get the column type
            col = mapper.columns[field]
            
            # Convert based on type
            if isinstance(col.type, INTEGER):
                try:
                    value = int(value)
                except (ValueError, TypeError):
                    raise ValueError(f"Invalid integer value for {field}: {value}")
            elif isinstance(col.type, Float):
                try:
                    value = float(value)
                except (ValueError, TypeError):
                    raise ValueError(f"Invalid float value for {field}: {value}")
                    
            setattr(user, field, value)
        
        await self.session.commit()
        return user
        

    async def get_by_user_id(self, user_id: int, *user_options) -> User | None:
        q = (
            select(User)
            .where(User.id == user_id)
            .options(*[selectinload(i) for i in user_options])
        )

        return (await self.session.execute(q)).scalar()
    
    async def get_info_by_user_id(self, user_id: int, *user_options) -> User | None:
        q = (
            select(User.age, User.rost, User.sex, User.ves, User.zabol)
            .where(User.id == user_id)
            .options(*[selectinload(i) for i in user_options])
        )

        return (await self.session.execute(q)).scalar()

    async def get_users_by_username(
        self, username: str, *user_options
    ) -> Sequence[User]:
        q = (
            select(User)
            .where(User.username == username)
            .options(*[selectinload(i) for i in user_options])
        )

        return (await self.session.execute(q)).scalars().all()


    async def get_all_users(self) -> Sequence[User]:
        q = select(User) 
        return (await self.session.execute(q)).scalars().all() 
    

    async def add_sex(self, user_id: int, sex: str):
        return await self.update_user_field(user_id, sex=sex)


    async def add_age(
            self, user_id: int, age: int
    ):
        return await self.update_user_field(user_id, age=age)

    async def add_ves(
            self, ves: float, user_id: int
    ):
        return await self.update_user_field(user_id, ves=ves)

    async def add_rost(
            self, rost: float, user_id: int
    ):
        return await self.update_user_field(user_id, rost=rost)

    
    async def add_zab(
            self, zab: str, user_id: int
    ):
       return await self.update_user_field(user_id, zabol=zab)

    