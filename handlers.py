from db import db, get_or_create_user, chek_admin
from utils import main_keyboard, admin_keyboard


def greet_user(update, context):
    print('вызван/start')
    # user = get_or_create_user(db, update.effective_user,
    #                           update.message.chat.id)
    update.message.reply_text(
          f"Здравствуй, пользователь! выбери кто ты?",
          reply_markup=main_keyboard()
          )


def admin_bot(update, context):
    print('кто то вызвал админа')
    user = chek_admin(db, update.effective_user,
                              update.message.chat.id) 
    if user:
        print('пришел админ')
        update.message.reply_text(
            f"Здравствуй, Админ! ",
            reply_markup=admin_keyboard()
            )
    else:
        update.message.reply_text("не понимаю комманду!")

# def helloo (update,context):
#     user = get_or_create_user(db, update.effective_user,update.message.chat.id)
#     print (context)
#     print(update['message']['chat']['id'])
#     print(update['message']['chat']['username'])

#     update.message.reply_text("Здравствуй, пользователь, выбери кто ты?")
#     return 'status'