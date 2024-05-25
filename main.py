import asyncio
import logging
import sys

from aiogram.client.default import DefaultBotProperties
from aiohttp import web

from aiogram.types import BotCommand

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from config import TELEGRAM_TOKEN, BASE_WEBHOOK_URL, WEBHOOK_PATH, WEB_SERVER_HOST, WEB_SERVER_PORT
from telegram_app.handlers import router


logger = logging.getLogger(__name__)

COMMANDS = [
    BotCommand(command='start', description='Начать'),
    BotCommand(command='help', description='Помощь'),
]


# bot = Bot(token=TELEGRAM_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
# dp = Dispatcher()

# async def main() -> None:
#     dp.include_router(router)
#     await bot.set_my_commands(COMMANDS)
#     await dp.start_polling(bot)
#
# if __name__ == "__main__":
#     asyncio.run(main())



async def on_startup(bot: Bot) -> None:
    await bot.set_webhook(
        f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}",
        # secret_token=WEBHOOK_SECRET,
    )
    logger.warning(f'Вебхук задан: {await bot.get_webhook_info()}')



async def on_shutdown(bot):
    await bot.delete_webhook()
    logger.warning(f'Вебхук удален')


def main() -> None:
    dp = Dispatcher()
    dp.include_router(router)

    # При запуске приложения
    dp.startup.register(on_startup)

    # При закрытии приложения
    dp.shutdown.register(on_shutdown)

    bot = Bot(TELEGRAM_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    app = web.Application()

    webhook_requests_handler = SimpleRequestHandler(  # TokenBasedRequestHandler
        dispatcher=dp,
        bot=bot,
        # secret_token=WEBHOOK_SECRET,
    )
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)
    try:
        logger.info(f'Приложение запущено')
        web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)
    except Exception as e:
        logger.error(e)





if __name__ == "__main__":
    logging.basicConfig(
        filename='log/log.log',
        level=logging.INFO,
        encoding='utf-8',
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%m.%d.%Y',
    )
    main()
