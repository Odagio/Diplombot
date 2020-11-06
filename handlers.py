from db import db, get_or_create_user, chek_admin, subscribe_user, unsubscribe_user, get_or_create_own, subscribe_own_db, unsubscribe_own_db
from utils import main_keyboard, admin_keyboard


def greet_user(update, context):
    print('вызван/start')
    # user = get_or_create_user(db, update.effective_user,
    #                           update.message.chat.id)
    update.message.reply_text(
          f"Здравствуй, пользователь! выбери кто ты?",
          reply_markup=main_keyboard()
          )


# def admin_bot(update, context):
#     print('кто то вызвал админа')
#     user = chek_admin(db, update.effective_user,
#                               update.message.chat.id) 
#     if user:
#         print('пришел админ')
#         update.message.reply_text(
#             f"Здравствуй, Админ! ",
#             reply_markup=admin_keyboard()
#             )
#     else:
#         update.message.reply_text("не понимаю комманду!")

def admin_bot(update, context):
    print('кто то вызвал админа')
    user = chek_admin(db, update.effective_user,
                              update.message.chat.id) 
    if user:
        print('пришел админ')
        update.message.reply_text(
            f"Здравствуй, Админ! напиши сообщение стажерам "            
            )
    else:
        update.message.reply_text("не понимаю комманду!")

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
