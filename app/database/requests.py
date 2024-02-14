from app.database.models import User, Product, Category, async_session
from sqlalchemy import select, update, delete


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
