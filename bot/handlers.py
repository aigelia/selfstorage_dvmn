from telegram import InlineKeyboardMarkup, InlineKeyboardButton

import menu_constants


def build_keyboard(action_type, button_rows):
    """Создает клавиатуру, принимает тип действия (для callback_data) и список списков с названиями кнопок."""
    keyboard = [
        [InlineKeyboardButton(text=button_label, callback_data=f"{action_type}_{row_index}")]
        for row_index, [button_label] in enumerate(button_rows)
    ]
    return InlineKeyboardMarkup(keyboard)


def back_to_menu():
    """Создает кнопку возврата в главное меню."""
    keyboard = [[InlineKeyboardButton(text='⬅️ Вернуться в главное меню', callback_data='to_menu')]]
    return InlineKeyboardMarkup(keyboard)


def handle_back_to_menu(update, context, param=None):
    """Обработчик кнопки возврата в главное меню."""
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text="📦 Что вас интересует?",
        reply_markup=build_keyboard('main_menu', menu_constants.MAIN_MENU)
    )


def handle_agreement(update, context, param=None):
    """Обработчик персонального соглашения."""
    query = update.callback_query
    query.answer()

    if param == '0':
        query.edit_message_text(
            text="Благодарим за согласие! 📦 Что вас интересует?",
            reply_markup=build_keyboard('main_menu', menu_constants.MAIN_MENU)
        )
    else:
        query.edit_message_text(
            text="К сожалению, в соответствии с российскими законами, мы не можем продолжать работу без Вашего согласия. Если Вы передумали, нажмите /start."
        )


def handle_main_menu(update, context, param=None):
    """Обработчик кнопок главного меню."""
    query = update.callback_query
    query.answer()

    if param == '0':
        handle_start_reservation(update, context)
    elif param == '1':
        handle_storage_rules(update, context)
    elif param == '2':
        handle_show_my_storages(update, context)
    elif param == '3':
        handle_take_my_stuff(update, context)
    else:
        query.edit_message_text(
            text="Что вас интересует?",
            reply_markup=build_keyboard('main_menu', menu_constants.MAIN_MENU)
        )

# ниже пока заглушки
def handle_start_reservation(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text="✍️ Как вас зовут? (Здесь будет сценарий бронирования ячейки)",
        reply_markup=back_to_menu()
    )


def handle_storage_rules(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text="Здесь будут правила хранения",
        reply_markup=back_to_menu()
    )


def handle_show_my_storages(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text="Здесь будут забронированные ячейки",
        reply_markup=back_to_menu()
    )


def handle_take_my_stuff(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text="Здесь будет QR-код для разблокировки ячейки",
        reply_markup=back_to_menu()
    )