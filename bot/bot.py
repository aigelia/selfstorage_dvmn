import os
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
import handlers
from menu_constants import MAIN_MENU


HANDLER_MAP = {
    'to_menu': bot_utils.handle_back_to_menu,
    'main_menu': bot_utils.handle_main_menu,
    'show_storage_rules': bot_utils.handle_show_storage_rules,
    'order_storage': bot_utils.handle_order_storage,
    'retrieve_items': bot_utils.handle_retrieve_items,
}

def start(update, context):
    update.message.reply_text(
        '''SelfStorage поможет вам сохранить то, что не умещается дома!
        🧥 Зимние вещи, когда на дворе лето
        🛷 Сноуборд, шины, велосипеды
        📦 Вещи на время переезда
        👶 Детские вещи «на потом»
        🗄 Документы и архивы (для бизнеса)
        🧳 Всё, что жалко выбросить, но негде держать
        Выберите нужный вам пункт меню:''',
        reply_markup=bot_utils.build_keyboard('main_menu', MAIN_MENU)
    )

def button_handler(update, context):
    query = update.callback_query
    query.answer()
    data = query.data.strip()
    
    handler = HANDLER_MAP.get(data)
    if handler:
        handler(update, context)  # Передаем только update и context
    else:
        query.edit_message_text('Выбор не распознан, нажмите /start для начала.')


def main():
    tg_token = '7988710995:AAHQXwvQbWwkIlqmYcu0EKsWVao_wAHgM6M'
    updater = Updater(tg_token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CallbackQueryHandler(button_handler))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
