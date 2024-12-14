"""User repository file."""

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.structures.role import Role

from ..models import Base, User
from .abstract import Repository


class UserRepo(Repository[User]):
    """User repository for CRUD and other SQL queries."""

    def __init__(self, session: AsyncSession):
        """Initialize user repository as for all users or only for one user."""
        super().__init__(type_model=User, session=session)

    async def new(
        self,
        user_id: int,
        user_name: str | None = None,
        full_name: str | None = None,
        phone_number: str | None = None,
        language: str | None = None,
        is_premium: bool | None = False,
        role: Role | None = Role.USER,
    ) -> None:
        """Insert a new user into the database.

        :param user_id: Telegram user id
        :param user_name: Telegram username
        :param full_name: Full name
        :param phone_number: Phone number
        :param is_premium: Telegram user premium status
        :param role: User's role
        :param user_chat: Telegram chat with user.
        """
        await self.session.merge(
            User(
                user_id=user_id,
                user_name=user_name,
                full_name=full_name,
                phone_number=phone_number,
                language_code=language,
                is_premium=is_premium,
                role=role,
            )
        )
        await self.session.commit()

    async def get_me(self, user_id: int) -> User:
        """Get user role by id."""
        user = await self.session.scalar(
            select(User).where(User.user_id == user_id).limit(1)
        )
        return user
    
    async def update_user(self, user_id: int, **kwargs) -> User:
        """Update user by id with new data."""
        async with self.session.begin():
            stmt = (
                update(User)
                .where(User.user_id == user_id)
                .values(**kwargs)
            )
            await self.session.execute(stmt)
            await self.session.commit()
