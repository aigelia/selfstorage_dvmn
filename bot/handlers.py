from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
import menu_constants

def handle_main_menu(update, context):
    """Обработчик для отображения главного меню."""
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        '''SelfStorage поможет вам сохранить то, что не умещается дома!
        🧥 Зимние вещи, когда на дворе лето
        🛷 Сноуборд, шины, велосипеды
        📦 Вещи на время переезда
        👶 Детские вещи «на потом»
        🗄 Документы и архивы (для бизнеса)
        🧳 Всё, что жалко выбросить, но негде держать
         Выберите нужный вам пункт меню:''',
        reply_markup=build_keyboard('main_menu', menu_constants.MAIN_MENU)
    )

def build_keyboard(action_type, button_rows):
    """Создает клавиатуру."""
    keyboard = []
    
    for row in button_rows:
        keyboard_row = []
        for label in row:
            if label == "Заказать хранение":
                callback_data = 'order_storage'
            elif label == "Забрать вещи":
                callback_data = 'retrieve_items'
            elif label == "Ознакомиться с правилами хранения":
                callback_data = 'show_storage_rules'
            else:
                callback_data = None  # Если нет соответствия
            
            keyboard_row.append(InlineKeyboardButton(label, callback_data=callback_data))
        
        keyboard.append(keyboard_row)
    
    return InlineKeyboardMarkup(keyboard)

def handle_show_storage_rules(update, context):
    """Отображение правил хранения"""
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        "Ссылка на правила хранения: [Правила хранения PDF](http://example.com/rules)",
        parse_mode='Markdown',
        reply_markup=build_keyboard('main_menu', menu_constants.MAIN_MENU)
    )


def handle_retrieve_items(update, context):
    """Обработчик для забирания вещей"""
    query = update.callback_query
    query.answer()
    qr_code_image_path = "C:/Users/andre/Documents/GitHub/SelfStorageBot/qr_code_image.png"
    query.edit_message_text("Вы можете забрать свои вещи, отсканировав этот QR-код на нашем складе. "
                            "Вы можете использовать этот QR-код в будущем, чтобы вернуть вещи в ячейку или взять из нее что-то нужное снова!")
    context.bot.send_photo(chat_id=query.message.chat.id, photo=open(qr_code_image_path, 'rb'))

def handle_back_to_menu(update, context):
    """Обработчик для возврата в главное меню."""
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        "Вы вернулись в главное меню.",
        reply_markup=build_keyboard('main_menu', menu_constants.MAIN_MENU)
    )
