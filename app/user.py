from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

import app.database.requests as db
import app.keyboards as kb
import app.states as st
import re
import datetime

user = Router()

# user.message.middleware(BaseMiddleware())

@user.callback_query(F.data == 'sure_cancel')
@user.callback_query(F.data == 'cancel')
@user.callback_query(F.data == 'back_from_events_list')
@user.message(CommandStart())
async def cmd_start(event: Message | CallbackQuery):
    if isinstance(event, Message):
        await db.set_user(event.from_user.id)
        await event.answer('Добро пожаловать в бот!', reply_markup=kb.main_kb)
    elif isinstance(event, CallbackQuery):
        await event.answer('Главная')
        await event.message.edit_text('Добро пожаловать в бот!', reply_markup=kb.main_kb)


@user.callback_query(F.data == 'events_list')
async def show_events_list(callback: CallbackQuery):
    await callback.answer('Список событий')
    events = await db.get_user_events(callback.from_user.id)
    if events:
        events_list = [f"{event.name} - {event.date.strftime('%d.%m.%Y')}" for event in events]
        events_message = '\n'.join(events_list)
    else:
        events_message = "У вас нет событий."
    await callback.message.edit_text(f'Ваши события:\n\n{events_message}', reply_markup=kb.back_from_events_list_kb)


"""

Добавление события!

"""
@user.callback_query(F.data == 'add_event')
async def show_events_list(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Добавление события')
    await state.set_state(st.AddEventState.name)
    await callback.message.edit_text('Введите название события', reply_markup=kb.cancel_kb)


@user.message(st.AddEventState.name)
async def event_name(message: Message, state: FSMContext):
    if len(message.text) > 100:
        await message.answer('❌ Название слишком длинное! Максимум 100 символов.')
    else:
        await state.update_data(name=message.text)
        await state.set_state(st.AddEventState.date)
        await message.answer(f'Введите дату события в формате дд.мм.гггг')


@user.message(st.AddEventState.date)
async def add_event_date(message: Message, state: FSMContext):
    date_text = message.text.strip()
    if not re.fullmatch(r"\d{2}\.\d{2}\.\d{4}", date_text):
        await message.answer('❌ Введите дату события в формате дд.мм.гггг')
        return
    try:
        parsed_date = datetime.datetime.strptime(date_text, "%d.%m.%Y").date()
    except ValueError:
        await message.answer('❌ Некорректная дата. Убедитесь, что такая дата существует.')
        return
    event_date = parsed_date.strftime("%d.%m.%Y")
    await state.update_data(date=parsed_date)
    tdata = await state.get_data()
    # устанавливаем нужное FSM состояние
    await state.set_state(st.AddEventState.sure)
    await message.answer(f'Вы уверены, что хотите добавить следующее событие?\n\n'
                         f'<b>Название</b>: {tdata['name']}\n'
                         f'<b>Дата</b>: {tdata['date'].strftime("%d.%m.%Y")}',
                         reply_markup=kb.sure_kb)


@user.callback_query(F.data == 'sure_yes', st.AddEventState.sure)
async def ok_add_event(callback: CallbackQuery, state: FSMContext):
    try:
        # берём данные из всех состояний
        tdata = await state.get_data()
        # добавляем новый заказ в БД
        await db.add_event(callback.from_user.id ,tdata['name'], tdata['date'])
        await callback.answer('Новое событие успешно добавлено')
        await callback.message.edit_text('Новое событие успешно добавлено', reply_markup=kb.main_kb)
    except Exception as e:
        await callback.message.answer(f'⚠️ {str(e)}')


"""

Удаление события!

"""
@user.callback_query(F.data == 'delete_event')
async def show_events_list(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Добавление события')
    await state.set_state(st.DeleteEventState.event_id)
    await callback.message.edit_text('Выберете событие, которое хотите удалить',
                                     reply_markup= await kb.events_list(callback.from_user.id))


@user.callback_query(F.data.startswith('delete-event_'), st.DeleteEventState.event_id)
async def sure_delete_event(callback: CallbackQuery, state: FSMContext):
    event_id = callback.data.split('_')[1]
    await state.update_data(event_id=event_id)
    # устанавливаем нужное FSM состояние
    await state.set_state(st.DeleteEventState.sure)
    await callback.message.edit_text(f'Вы уверены, что хотите удалить событие?',
                         reply_markup=kb.sure_kb)


@user.callback_query(F.data == 'sure_yes', st.DeleteEventState.sure)
async def ok_delete_event(callback: CallbackQuery, state: FSMContext):
    try:
        # берём данные из всех состояний
        tdata = await state.get_data()
        # добавляем новый заказ в БД
        await db.delete_event(tdata['event_id'])
        await callback.answer('Событие удалено')
        await callback.message.edit_text('Событие удалено', reply_markup=kb.main_kb)
    except Exception as e:
        await callback.message.answer(f'⚠️ {str(e)}')