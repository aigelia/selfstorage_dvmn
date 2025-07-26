from telegram import InlineKeyboardMarkup, InlineKeyboardButton

import getters
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
    elif param == '4':
        handle_legal_services(update, context)
    else:
        query.edit_message_text(
            text="Что вас интересует?",
            reply_markup=build_keyboard('main_menu', menu_constants.MAIN_MENU)
        )


def handle_start_reservation(update, context, param=None):
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text="✍️ Как вас зовут?",
        reply_markup=back_to_menu()
    )
    context.user_data['current_step'] = 'ask_name'


def handle_ask_name(update, context, param=None):
    user_data = context.user_data
    user_name = update.message.text.strip()

    user_data['name'] = user_name

    update.message.reply_text(
        f"🏢 Выберите удобный склад:",
        reply_markup=build_keyboard('choose_warehous', menu_constants.WAREHOUSES)
    )

    user_data['current_step'] = 'choose_warehouse'


def handle_choose_warehouse(update, context, param=None):
    query = update.callback_query
    query.answer()

    context.user_data['warehouse'] = menu_constants.WAREHOUSES[int(param)]

    query.edit_message_text(
        text='Вам нужна помощь с доставкой вещей до склада?',
        reply_markup=build_keyboard('delivery_type', menu_constants.DELIVERY_TYPE)
    )

    context.user_data['current_step'] = 'delivery_type'


def handle_delivery_type(update, context, param=None):
    query = update.callback_query
    query.answer()

    context.user_data['delivery_type'] = menu_constants.DELIVERY_TYPE[int(param)]

    if param == '0':
        query.edit_message_text(
            text="С какой даты вы планируете начать аренду?",
            # TODO даты на ближайшую неделю из бд reply_markup=...
        )

        context.user_data['current_step'] = 'specify_rental_start_date'
    else:
        query.edit_message_text(
            text="Укажите адрес, откуда забрать вещи:",
            reply_markup=back_to_menu()
        )

        context.user_data['current_step'] = 'specify_address'


# Продолжить отсюда!!!


def handle_specify_address(update, context, param=None):
    pass


def handle_specify_phone_number(update, context, param=None):
    pass


def handle_courier_meeting_date(update, context, param=None):
    pass


def handle_specify_rental_start_date(update, context, param=None):
    pass


def handle_cell_size(update, context, param=None):
    pass


def handle_period_of_storage(update, context, param=None):
    pass


def handle_show_storage_info(update, context, param=None):
    pass


# Конец тут !!!


def handle_storage_rules(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=menu_constants.STORAGE_RULES, reply_markup=back_to_menu())


def handle_show_my_storages(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text=getters.get_my_storages(),
        reply_markup=back_to_menu()
    )

    # TODO проверить корректность ответа


def handle_take_my_stuff(update, context):
    query = update.callback_query
    query.answer()

    query.delete_message()

    context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo="https://api.qrserver.com/v1/create-qr-code/?size=250x250&data=SelfStorageAccess",
        caption=(
            "📲 Вы можете забрать свои вещи, отсканировав этот QR-код на нашем складе.\n\n"
            "Этот QR-код можно использовать и в будущем — чтобы вернуть вещи в ячейку "
            "или взять что-то нужное снова!"
        ),
        reply_markup=back_to_menu()
    )


def handle_legal_services(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text="Здесь будут услуги для юридических лиц",
        reply_markup=back_to_menu()
    )
    # TODO: создать и проработать сценарий для юридических лиц


# TODO подтянуть все возможное из БД