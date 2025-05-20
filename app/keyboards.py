from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
import app.database.requests as db


main_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Мои события', callback_data='events_list'),
     InlineKeyboardButton(text='Добавить событие', callback_data='add_event')],
    [InlineKeyboardButton(text='Изменить событие', callback_data='edit_event'),
     InlineKeyboardButton(text='Удалить событие', callback_data='delete_event')]])


back_from_events_list_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='back_from_events_list')]])


cancel_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Отмена', callback_data='cancel')]])


sure_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🌟 Да', callback_data='sure_yes'),
     InlineKeyboardButton(text='❌ Отмена', callback_data='sure_cancel')]])


sure = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='🌟 Да'),
                                      KeyboardButton(text='❌ Отмена')]],
                           resize_keyboard=True)  # параметр для отображения клавиатуры на разных устройствах


async def events_list(tg_id):
    events = await db.get_user_events(tg_id)
    kb = InlineKeyboardBuilder()
    for event in events:
        kb.add(InlineKeyboardButton(text=f"{event.name} - {event.date.strftime('%d.%m.%Y')}",
                                    callback_data=f"delete-event_{event.id}"))
    kb.add(InlineKeyboardButton(text='❌ Отмена', callback_data='cancel'))
    kb.adjust(1)
    return kb.as_markup()
