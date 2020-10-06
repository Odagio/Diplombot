import logging
from db import db, get_or_create_user, change_status, save_anketa
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import settings

logging.basicConfig(filename='bot.log', level=logging.INFO)


def helloo (update,context):
    user = get_or_create_user(db, update.effective_user,update.message.chat.id)
    print (context)
    print(update['message']['chat']['id'])
    print(update['message']['chat']['username'])

    update.message.reply_text("Здравствуй, пользователь, выбери кто ты?")
    return 'status'

states = ('start', 'name', 'city', 'email')
questions = {"start": "cтатус", "name":"как твое имя?","city":" из какого ты города?", "email":"скажи свою почту?"}

def talk_to_me (update, context):
    user = get_or_create_user(db, update.effective_user, update.message.text)
    current_stat = states.index(user.get('status'))
    next_stat = states[current_stat+1]

    change_status(user, next_stat)

    update.message.reply_text(questions.get(next_stat))

    user_text = update.message.text
    context.user_data['states'] = {'name': user_text}

    context.user_data["anketa"] = {next_stat: user_text}
    user = get_or_create_user(db, update.effective_user, update.message.chat_id)
    save_anketa(db, user['user_id'], context.user_data['anketa'])
    print(user_text)





def main():
  mybot = Updater(settings.API_KEY, use_context=True)
  dp = mybot.dispatcher
  dp.add_handler(CommandHandler('start', helloo))
  dp.add_handler(MessageHandler(Filters.text, talk_to_me))
  logging.info("Бот стартовал")
  mybot.start_polling()
  mybot.idle()

if __name__ == "__main__":
     main()
# x = mycol.insert_many(mylist)

# #print list of the _id values of the inserted documents:
# print(x.inserted_ids)