import os
import handlers

from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from menu_constants import MAIN_MENU


HANDLER_MAP = {
    'agreement_accepted': handlers.handle_agreement_accepted,
    'to_menu': handlers.handle_back_to_menu,
    'main_menu': handlers.handle_main_menu,
    'show_storage_rules': handlers.handle_show_storage_rules,
    'retrieve_items': handlers.handle_retrieve_items,
}


def start(update, context):
    """Обработчик /start с запросом согласия обработки пд"""
    handlers.show_agreement_request(update)


def button_handler(update, context):
    """Обработчик нажатий кнопок"""
    query = update.callback_query
    query.answer()
    data = query.data.strip()

    handler = HANDLER_MAP.get(data)
    if handler:
        handler(update, context)  # Передаем только update и context
    else:
        query.edit_message_text('Выбор не распознан, нажмите /start для начала.')


def main():
    load_dotenv()
    tg_token = os.getenv("TG_TOKEN")

    updater = Updater(tg_token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CallbackQueryHandler(button_handler))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
