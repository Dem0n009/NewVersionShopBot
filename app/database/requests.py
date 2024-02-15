from app.database.models import User, Product, Category, async_session
from sqlalchemy import select, update, delete


async def set_user(tg_id: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()


async def get_users():
    async with async_session() as session:
        result = await session.scalars(select(User))
        return result


async def get_categories():
    async with async_session() as session:
        result = await session.scalars(select(Category))
        return result


async def get_products(category_id: int):
    async with async_session() as session:
        result = await session.scalars(select(Product).where(Product.category == category_id))
        return result


async def get_product(product_id: int):
    async with async_session() as session:
        result = await session.scalar(select(Product).where(Product.id == product_id))
        return result
