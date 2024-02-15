from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command, Filter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import app.keyboards as kb
from app.database.requests import get_product, get_users

admin = Router()


class Newsletter(StatesGroup):
    message = State()


class AdminProtect(Filter):
    async def __call__(self, message: types.Message):
        return message.from_user.id in [953094525]


@admin.message(AdminProtect(), Command('apanel'))
async def apanel(message: types.Message):
    await message.answer(f'Возможные команды: /newsletter')


@admin.message(AdminProtect(), Command('newsletter'))
async def newsletter(message: types.Message, state: FSMContext):
    await state.set_state(Newsletter.message)
    await message.answer('Напишите текст сообщения, которое вы хотите разослать')


@admin.message(AdminProtect(), Newsletter.message)
async def send_newsletter(message: types.Message, state: FSMContext):
    await message.answer('Подождите... идёт рассылка')
    for user in await get_users():
        try:
            await message.send_copy(chat_id=user.tg_id)
        except:
            pass
    await message.answer('Рассылка завершена')
    await state.clear()
