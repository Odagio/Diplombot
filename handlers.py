from db import db, get_or_create_user, chek_admin, subscribe_user, unsubscribe_user, get_or_create_own, subscribe_own_db, unsubscribe_own_db
from utils import main_keyboard, admin_keyboard


def greet_user(update, context):
    print('вызван/start')
    update.message.reply_text(
          f"""Привет это бот Intrn.
Выпускники онлайн-курсов не могут устроиться после окончания обучения,
так как для работодателя важен реальный опыт работы. 
А без реальной работы не получить реальный опыт - получается замкнутый круг.
Мы собираемся этот круг разомкнуть!
Выбери из 2 вариантов ты стажер или у тебя есть продукт,
который ты хочешь проверить
""",
          reply_markup=main_keyboard()
          )


def subscribe(update, context):
    user = get_or_create_user(db, update.effective_user, update.message)
    subscribe_user(db, user)
    update.message.reply_text('Вы подписались')


def unsubscribe(update, context):
    user = get_or_create_user(db, update.effective_user, update.message)
    unsubscribe_user(db, user)
    update.message.reply_text('Вы отписались')


def own_subscribe(update, context):
    user = get_or_create_own(db, update.effective_user, update.message)
    subscribe_own_db(db, user)
    update.message.reply_text('Вы подписались')


def own_unsubscribe(update, context):
    user = get_or_create_own(db, update.effective_user, update.message)
    unsubscribe_own_db(db, user)
    update.message.reply_text('Вы отписались')
