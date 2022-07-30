import datetime

import telegram

from database import SuppliesManager, Supply
from settiings import (CHAT_ID_FOR_NOTIFICATION, DATETIME_FORMAT,
                       TELEGRAM_BOT_TOKEN)

bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)


def check_all_supplies():
    """Check that all supplies are in time.
    
    Send message to chat if supply is out of time.
    """
    supplies = SuppliesManager().get_all_supplies()
    for supply in supplies:
        check_supply(supply)


def check_supply(supply: Supply):
    """Check that supply is in time."""
    if supply.date < datetime.datetime.now():
        bot.send_message(chat_id=CHAT_ID_FOR_NOTIFICATION, text=f'Поставка {supply.order_number} просрочена!')


if __name__ == '__main__':
    check_all_supplies()
