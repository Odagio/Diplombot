import logging
from anketa_applicant import (anketa_start, anketa_name, anketa_city, anketa_skip, anketa_role, anketa_exp_role, anketa_tuition,
anketa_previous_exp, anketa_superpower, anketa_purpose, anketa_time_work, anketa_worth, anketa_contacts, anketa_skip,  anketa_comment, anketa_dontknow)
from db import db, get_or_create_user, save_anketa
from handlers import greet_user, admin_bot
from telegram.ext import Updater, CommandHandler, MessageHandler,ConversationHandler, Filters
import settings

logging.basicConfig(filename='bot.log', level=logging.INFO)


def main():
    mybot = Updater(settings.API_KEY, use_context=True)
    dp = mybot.dispatcher

    anketa = ConversationHandler(
      entry_points = [
        MessageHandler(Filters.regex('^(Стажер)$'), anketa_start)
      ],
      states = {
        "name": [MessageHandler(Filters.text, anketa_name)],
        "city": [MessageHandler(Filters.text, anketa_city)],
        "role": [MessageHandler(Filters.text, anketa_role)],
        "exp_role": [MessageHandler(Filters.text, anketa_exp_role)],
        "tuition": [MessageHandler(Filters.text, anketa_tuition)],
        "previous_exp": [MessageHandler(Filters.text, anketa_previous_exp)],
        "superpower": [MessageHandler(Filters.text, anketa_superpower)],
        "purpose": [MessageHandler(Filters.text, anketa_purpose)],
        "time_work": [MessageHandler(Filters.text, anketa_time_work)],
        "worth": [MessageHandler(Filters.text, anketa_worth)],
        "mail": [MessageHandler(Filters.text, anketa_contacts)],
        "contacts": [
        CommandHandler("skip", anketa_skip),
        MessageHandler(Filters.text, anketa_comment)
      ]
      },
      fallbacks = [
               MessageHandler(Filters.text | Filters.video | Filters.photo | Filters.document | Filters.location, anketa_dontknow)
      ] 
      )
    
    
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('admin', admin_bot))
    dp.add_handler(anketa)

    logging.info("Бот стартовал")
    mybot.start_polling()
    mybot.idle()

if __name__ == "__main__":
     main()
