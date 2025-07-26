import os

from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters

import handlers
from menu_constants import AGREEMENT, MAIN_MENU

HANDLER_MAP = {
    'agreement': handlers.handle_agreement,
    'to_menu': handlers.handle_back_to_menu,
    'main_menu': handlers.handle_main_menu,
    'ask_name': handlers.handle_ask_name,
    'choose_warehouse': handlers.handle_choose_warehouse,
}


def start(update, context):
    """Обработчик команды /start."""
    update.message.reply_text(
        'SelfStorage поможет вам сохранить то, что не умещается дома!\n\n' 
        '🧥 Зимние вещи, когда на дворе лето\n'
        '🛷 Сноуборд, шины, велосипеды\n'
        '📦 Вещи на время переезда\n'
        '👶 Детские вещи «на потом»\n'
        '🗄 Документы и архивы (для бизнеса)\n'
        '🧳 Всё, что жалко выбросить, но негде держать\n\n'
        'Чтобы продолжить, нам необходимо ваше согласие на обработку персональных данных в соответствии с политикой (ЗДЕСЬ БУДЕТ ССЫЛКА) SelfStorage\n',
        reply_markup=handlers.build_keyboard('agreement', AGREEMENT)
    )


def button_handler(update, context):
    """Общий обработчик нажатий кнопок."""
    query = update.callback_query
    query.answer()
    data = query.data.strip()

    if data in HANDLER_MAP:
        action = data
        param = None
    else:
        if '_' in data:
            action, param = data.rsplit('_', 1)
        else:
            action = data
            param = None
    handler = HANDLER_MAP.get(action)
    if handler:
        handler(update, context, param)
    else:
        query.edit_message_text('Выбор не распознан, нажмите /start для начала.')


def message_handler(update, context):
    """Обработчик текстового сообщения."""
    current_step = context.user_data.get('current_step')

    if current_step and current_step in HANDLER_MAP:
        HANDLER_MAP[current_step](update, context)
        return


def run_bot():
    load_dotenv()
    tg_token = os.environ['TG_TOKEN']
    notifications_chat_id = os.environ['NOTIFICATIONS_CHAT_ID']

    updater = Updater(tg_token, use_context=True)
    dp = updater.dispatcher
    dp.bot_data['notifications_chat_id'] = notifications_chat_id
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CallbackQueryHandler(button_handler))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, message_handler))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    run_bot()
