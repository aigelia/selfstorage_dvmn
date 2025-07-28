from datetime import timedelta

from telegram import InlineKeyboardMarkup, InlineKeyboardButton

import getters
import menu_constants
from helpers import get_next_week_dates_keyboard, build_summary, to_date


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


def handle_start_reservation(update, context):
    """Начало бронирования - запрашиваем имя"""
    query = update.callback_query
    query.answer()
    context.user_data['user_id'] = update.effective_user.id
    getters.create_or_update_client(user_id=update.effective_user.id)

    query.edit_message_text(
        text="✍️ Как вас зовут?"
    )
    context.user_data['current_step'] = 'ask_name'
    context.user_data['is_legal'] = False


def handle_ask_name(update, context):
    user_data = context.user_data
    user_name = update.message.text.strip()

    user_data['full_name'] = user_name
    user_id = update.effective_user.id
    getters.create_or_update_client(
        user_id=user_id,
        full_name=user_name
    )


    update.message.reply_text(
        "🏢 Выберите удобный склад:",
        reply_markup=build_keyboard('choose_warehouse', getters.get_warehouses())
    )
    context.user_data['current_step'] = 'choose_warehouse'


def handle_choose_warehouse(update, context, param=None):
    query = update.callback_query
    query.answer()

    context.user_data['warehouse'] = getters.get_warehouses()[int(param)][0]

    query.edit_message_text(
        text='Вам нужна помощь с доставкой вещей до склада?',
        reply_markup=build_keyboard('delivery_type', menu_constants.DELIVERY_TYPE)
    )

    context.user_data['current_step'] = 'delivery_type'


def handle_delivery_type(update, context, param=None):
    query = update.callback_query
    query.answer()

    context.user_data['delivery_type'] = menu_constants.DELIVERY_TYPE[int(param)]
    context.user_data['using_courier'] = False

    if param == '0':  # сам везёт
        query.edit_message_text(
            text="📅 С какой даты вы планируете начать аренду?",
            reply_markup=get_next_week_dates_keyboard('specify_rental_start_date')
        )
        context.user_data['current_step'] = 'specify_rental_start_date'

    else:
        query.edit_message_text(
            text="🏠 Укажите адрес, откуда забрать вещи:",
        )

        context.user_data['current_step'] = 'specify_address'


def handle_specify_address(update, context, param=None):
    user_data = context.user_data
    user_address = update.message.text.strip()

    user_data['address'] = user_address
    user_data['using_courier'] = True

    getters.create_or_update_client(
        user_id=context.user_data['user_id'],
        address=user_address
    )

    update.message.reply_text(
        f"📞 Ваш номер телефона для связи с курьером:",
    )

    user_data['current_step'] = 'specify_phone_number'


def handle_specify_phone_number(update, context, param=None):
    user_data = context.user_data
    user_phone_number = update.message.text.strip()

    user_data['phone_number'] = user_phone_number

    getters.create_or_update_client(
        user_id=user_data['user_id'],
        phone_number=user_phone_number
    )

    update.message.reply_text(
        "📅 Когда удобно встретить доставщика?",
        reply_markup=get_next_week_dates_keyboard("select_start_date")
    )

    user_data['current_step'] = 'specify_rental_start_date'


def handle_specify_rental_start_date(update, context, param=None):
    print(param)
    user_data = context.user_data
    query = update.callback_query
    query.answer()

    context.user_data['rental_start_date'] = param

    if user_data.get('is_legal') is True:
        user_data['is_legal'] = False
        query.edit_message_text(
            text="Сколько стеллажей вам понадобится?",
            reply_markup=build_keyboard('cell_size', menu_constants.RACKS)
        )

    else:
        query.edit_message_text(
            text="Какого размера ячейка вам понадобится?",
            reply_markup=build_keyboard('cell_size', menu_constants.CELLS) # TODO вытащить из бд
        )

    context.user_data['current_step'] = 'cell_size'


def handle_cell_size(update, context, param=None):
    query = update.callback_query
    query.answer()

    user_data = context.user_data

    if user_data.get('is_legal'):
        user_data['cell_size'] = menu_constants.RACKS[int(param)][0]
    else:
        user_data['cell_size'] = menu_constants.CELLS[int(param)][0]

    query.edit_message_text(
        text="Какой срок хранения вас интересует?",
        reply_markup=build_keyboard('period_of_storage', menu_constants.STORAGE_PERIODS)
    )

    user_data['current_step'] = 'period_of_storage'


def handle_period_of_storage(update, context, param=None):
    query = update.callback_query
    query.answer()

    rental_start_date_str = context.user_data.get('rental_start_date')
    rental_start_date = to_date(rental_start_date_str)

    if not rental_start_date:
        query.edit_message_text("Ошибка: дата начала аренды не выбрана или указана неверно.")
        return

    period_days = menu_constants.STORAGE_PERIODS[int(param)]
    period_of_storage = rental_start_date + timedelta(days=period_days)

    context.user_data['period_of_storage'] = period_of_storage.isoformat()

    summary_text = build_summary(context.user_data)

    price_placeholder = "..."  # TODO: заменить на реальный расчет
    rules_link = "[ССЫЛКА НА PDF]"
    policy_link = "[ССЫЛКА НА PDF]"

    if context.user_data.get('using_courier'):
        extra_text = (
            f"\n\n💰 Стоимость хранения: {price_placeholder} рублей.\n\n"
            f"📎 Перед оформлением, пожалуйста, ознакомьтесь:\n"
            f"- с правилами хранения {rules_link},\n"
            f"- списком разрешенных и запрещенных вещей,\n"
            f"- политикой обработки персональных данных {policy_link}."
        )
    else:
        extra_text = (
            f"\n\n💰 Стоимость хранения: {price_placeholder} рублей.\n\n"
            f"📎 Ознакомьтесь с правилами хранения {rules_link} и политикой конфиденциальности {policy_link}."
        )

    query.edit_message_text(
        text=summary_text + extra_text,
        parse_mode='HTML',
        reply_markup=build_keyboard('show_storage_info', menu_constants.AGREEMENT_TO_ORDER)
    )

    context.user_data['current_step'] = 'show_storage_info'


def handle_show_storage_info(update, context, param=None):
    query = update.callback_query
    query.answer()

    if param == '0':
        query.edit_message_text(
            text='Ваш заказ успешно создан!',
            reply_markup=back_to_menu()
        )
    else:
        query.edit_message_text(
            text='Ваш заказ успешно отменен!',
            reply_markup=back_to_menu()
        )


def handle_storage_rules(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=menu_constants.STORAGE_RULES, reply_markup=back_to_menu())


def handle_show_my_storages(update, context):
    query = update.callback_query
    query.answer()
    user_id = update.effective_user.id
    query.edit_message_text(
        text=getters.get_my_storages(user_id=user_id),
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
    keyboard = [
        [
            InlineKeyboardButton("Продолжить", callback_data="continue_legal_service"),
            InlineKeyboardButton("Вернуться в главное меню", callback_data="to_menu")
        ]
    ]
    query.edit_message_text(
        text=(
            "📦 SelfStorage предоставляет услуги по хранению документов для юридических лиц.\n"
            "Стоимость аренды одного стеллажа составляет 899 рублей в месяц.\n"
            "Вы бы хотели приобрести эту услугу?"
        ),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


def handle_continue_legal_services(update, context, param=None):
    query = update.callback_query
    query.answer()

    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text="✍️ Как вас зовут?"
    )
    context.user_data['current_step'] = 'ask_name'
    context.user_data['is_legal'] = True

    # TODO: создать и проработать сценарий для юридических лиц


# TODO подтянуть все возможное из БД