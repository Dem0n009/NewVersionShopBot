from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

import app.keyboards as kb
from app.database.requests import get_product

router = Router()


@router.message(CommandStart())
@router.callback_query(F.data == 'to_main')
async def cmd_start(message: types.Message | types.CallbackQuery):
    if isinstance(message, types.Message):
        await message.answer(f"Здравствуйте, {message.from_user.full_name}!", reply_markup=kb.main)
    else:
        await message.message.edit_text(f"Здравствуйте, {message.from_user.full_name}!", reply_markup=kb.main)


@router.callback_query(F.data == 'catalog')
async def catalog(callback: types.CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text(f'Выбирете вариант из каталога', reply_markup=await kb.categories())


@router.callback_query(F.data.startswith('category_'))
async def category_selected(callback: types.CallbackQuery):
    category_id = callback.data.split('_')[1]
    await callback.message.edit_text(f'Товары по выбранной категории', reply_markup=await kb.products(category_id))


@router.callback_query(F.data.startswith('product_'))
async def product_selected(callback: types.CallbackQuery):
    product = await get_product(callback.data.split('_')[1])
    await callback.answer('')
    await callback.message.edit_text(f'{product.name}\n\n Цена: {product.price} рублей', reply_markup=kb.to_main)
