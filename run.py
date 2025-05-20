import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.user import user
from app.admin import admin

from config import TOKEN

from app.database.models import async_main
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import datetime
from app.apshed import check_event_start_date, check_event_start_date_in_3_days, check_event_start_date_in_7_days


async def main():
    bot = Bot(token=TOKEN,
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    
    dp = Dispatcher()
    dp.include_routers(user, admin)
    dp.startup.register(startup)
    dp.shutdown.register(shutdown)

    """

    Создаём ежедневно повторяющиеся действия
    ----------------------------------------------------------------------------------------------
    """

    # создаём объект расписания с установкой часового пояса (scheduler)
    # scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler = AsyncIOScheduler(timezone="Asia/Novosibirsk")

    # варианты добавления задач, которые сработают через минуту и 2 минуты соответсвенно

    scheduler.add_job(check_event_start_date, trigger='cron', hour=datetime.datetime.now().hour,
                      minute=datetime.datetime.now().minute+1, start_date=datetime.datetime.now(), kwargs={'bot': bot})
    scheduler.add_job(check_event_start_date_in_3_days, trigger='cron', hour=datetime.datetime.now().hour,
                      minute=datetime.datetime.now().minute + 2, start_date=datetime.datetime.now(),
                      kwargs={'bot': bot})
    scheduler.add_job(check_event_start_date_in_7_days, trigger='cron', hour=datetime.datetime.now().hour,
                      minute=datetime.datetime.now().minute + 3, start_date=datetime.datetime.now(),
                      kwargs={'bot': bot})

    # добавляем задачи и устанавливаем нужный час и минуту, при наступлении которых задачи будут срабатывать
    # задача для удаления аренды с истёкшим сроком
    # scheduler.add_job(check_subscription_end_date, trigger='cron', hour=16, minute=37, kwargs={'bot': bot})
    # # задача для уведомления пользователей, что до окончания аренды остался 1 день
    # scheduler.add_job(update_the_number_of_responses, trigger='cron', hour=16, minute=18, kwargs={'bot': bot})
    scheduler.start()  # запускаем планировщик
    
    await dp.start_polling(bot)


async def startup(dispatcher: Dispatcher):
    await async_main()
    print('Starting up...')


async def shutdown(dispatcher: Dispatcher):
    print('Shutting down...')


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
