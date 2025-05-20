from aiogram import Bot
import app.database.requests as db


async def check_event_start_date(bot: Bot):
    events_with_start_today = await db.events_with_start_today()
    for event in events_with_start_today:
        await bot.send_message(event.user.tg_id, f'<b>Сегодня {event.name}!</b>')


async def check_event_start_date_in_3_days(bot: Bot):
    events_start_date_in_3_days = await db.events_start_date_in_3_days()
    for event in events_start_date_in_3_days:
        await bot.send_message(event.user.tg_id, f'<b>Осталось 3 дня до {event.name}!</b>')


async def check_event_start_date_in_7_days(bot: Bot):
    events_start_date_in_7_days = await db.events_start_date_in_7_days()
    for event in events_start_date_in_7_days:
        await bot.send_message(event.user.tg_id, f'<b>Осталось 7 дней до {event.name}!</b>')

