import os
from typing import List

from dotenv import load_dotenv
from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import relationship, Mapped, DeclarativeBase, mapped_column

load_dotenv()
db = os.getenv('SQLALCHEMY_DATABASE_URI')

engine = create_async_engine(url=db, echo=True)

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)

    basket_rel: Mapped[List['Basket']] = relationship(back_populates='user_rel')


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    product_rel: Mapped[List['Product']] = relationship(back_populates='category_rel')


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(200))
    category: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    photo: Mapped[str] = mapped_column(String(200))
    price: Mapped[int] = mapped_column()

    category_rel: Mapped['Category'] = relationship(back_populates='product_rel')
    basket_rel: Mapped[List['Basket']] = relationship(back_populates='product_rel')


class Basket(Base):
    __tablename__ = 'basket'

    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped[int] = mapped_column(ForeignKey('users.id'))
    product: Mapped[int] = mapped_column(ForeignKey('products.id'))

    user_rel: Mapped['User'] = relationship(back_populates='basket_rel')
    product_rel: Mapped['Product'] = relationship(back_populates='basket_rel')


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
