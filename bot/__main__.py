import logging
import sched, time

from datetime import datetime
from pathlib import Path
from aiogram import executor
from bot.handlers import *

def main():
    log_name = f'logs/{datetime.now().strftime("%Y-%m-%d")}.log'
    Path(log_name).parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        filename=log_name,
        filemode="a"
    )

    executor.start_polling(dp, skip_updates=True)

if __name__ == "__main__":
    main()