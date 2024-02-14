import datetime
import locale

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.requests import get_categories, get_products

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

main = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Каталог', callback_data='catalog')],
        [InlineKeyboardButton(text='Корзина', callback_data='basket'),
         InlineKeyboardButton(text='Контакты', callback_data='contacts')],
    ],

)

to_main = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='На главную', callback_data='to_main')]])


async def categories():
    categories = await get_categories()
    categories_kb = InlineKeyboardBuilder()
    for category in categories:
        categories_kb.add(InlineKeyboardButton(text=category.name, callback_data=f'category_{category.id}'))
    return categories_kb.adjust(2).as_markup()


async def products(category_id: int):
    products_kb = InlineKeyboardBuilder()
    products = await get_products(category_id)
    for product in products:
        products_kb.add(InlineKeyboardButton(text=product.name, callback_data=f'product_{product.id}'))
    return products_kb.adjust(2).as_markup()

#
# async def date_kb():
#     kb = InlineKeyboardBuilder()
#     current_date = datetime.date.today()
#     for i in range(14):
#         current_date += datetime.timedelta(days=1)
#         kb.button(text=f'{current_date.strftime("%d %B")}', callback_data=f'{current_date.strftime("%d.%m.%y")}')
#     kb.adjust(2)
#     return kb.as_markup()
#
#
# async def time_kb():
#     kb = InlineKeyboardBuilder()
#     for i in range(8, 18, 1):
#         kb.button(text=f'{i}:00', callback_data=f'time {i}:00')
#     kb.adjust(2)
#     return kb.as_markup()
