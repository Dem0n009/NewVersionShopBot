from aiogram import Router, types, F
from aiogram.filters import CommandStart

import app.keyboards as kb
from app.database.requests import get_product

router = Router()


@router.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(f"Здравствуйте, {message.from_user.full_name}!", reply_markup=await kb.date_kb())


@router.message(F.text == 'Каталог')
async def catalog(message: types.Message):
    await message.answer(f'Выбирете вариант из каталога', reply_markup=await kb.categories())


@router.callback_query(F.data.startswith('category_'))
async def category_selected(callback: types.CallbackQuery):
    category_id = callback.data.split('_')[1]
    await callback.message.answer(f'Товары по выбранной категории', reply_markup=await kb.products(category_id))
    await callback.answer(text=f'Выбрано!')


@router.callback_query(F.data.startswith('product_'))
async def product_selected(callback: types.CallbackQuery):
    product_id = callback.data.split('_')[1]
    product = await get_product(product_id=product_id)
    await callback.message.answer(f'{product.name}\n\n Цена: {product.price} $')
    await callback.answer(f'Вы выбрали {product.name}')

# @dp.message(Command("dice"))
# async def cmd_dice(message: types.Message, bot: Bot):
#     await bot.send_dice(-100123456789, emoji=DiceEmoji.DICE)
