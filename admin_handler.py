from db import (db, get_or_create_own,  get_or_create_user, get_subscribed, chek_admin,
               get_or_create_own, get_subscribed_own)
from telegram import ParseMode, ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler
from utils import admin_keyboard


def admin_start(update, context):
    user = chek_admin(db, update.effective_user,
                              update.message.chat.id) 
    if user:
        print('пришел админ')
        update.message.reply_text(
            f"Здравствуй, Админ! ", reply_markup=admin_keyboard()
            )
    else:
        update.message.reply_text("не понимаю комманду!")
    return 'choice'
     

def send_to_application(update, context):
    print ('im here')
    answer_admin = update.message.text 
    if answer_admin == '/applicants':
        update.message.reply_text("Пиши текст")
        return 'text_for_app'  


def admin_text_for_app(update, context):         
    admin_text = update.message.text
    for user in get_subscribed(db):
        context.bot.send_message(chat_id=user['chat_id'], text=f'{admin_text}')
    return ConversationHandler.END


def send_to_owns(update, context):
    print ('im here master')
    answer_admin = update.message.text 
    if answer_admin == '/owns':
        update.message.reply_text("Пиши текст")
        return 'text_for_own'  


def admin_text_for_own(update, context):
    print("настрой дб")         
    admin_text = update.message.text
    for user in get_subscribed_own(db):
        context.bot.send_message(chat_id=user['chat_id'], text=f'{admin_text}')
    return ConversationHandler.END
                       