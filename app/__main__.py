import asyncio
import logging
import sched, time

from datetime import datetime
from pathlib import Path
from app.dispatcher import bot, dp
from app.handlers import base, admin

async def main():
    dp.include_routers(base.router, admin.router)

    await dp.start_polling(bot, skip_updates=True)

if __name__ == '__main__':
    log_name = f'logs/{datetime.now().strftime("%Y-%m-%d")}.log'
    Path(log_name).parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        filename=log_name,
        filemode="a"
    )
    asyncio.run(main())