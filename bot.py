import logging
from anketa_applicant import (anketa_start, anketa_name, anketa_city, anketa_skip, anketa_role, anketa_exp_role, anketa_tuition,
anketa_previous_exp, anketa_superpower, anketa_purpose, anketa_time_work, anketa_worth, anketa_mail, anketa_skip,  anketa_contacts_end, anketa_dontknow, cancel)
from anketa_prod_owner import (anketa_start_own, anketa_own_name, anketa_own_city, anketa_own_project_name,
anketa_own_working_condition, anketa_own_mvp, anketa_own_presentation, anketa_own_team, anketa_own_mentor, anketa_own_mail,
anketa_own_skip, anketa_own_contacts_end   )
from db import db, get_or_create_user, save_anketa, save_own_anketa, get_or_create_own
from handlers import greet_user, admin_bot
from telegram.ext import Updater, CommandHandler, MessageHandler,ConversationHandler, Filters
import settings

logging.basicConfig(filename='bot.log', level=logging.INFO)


def main():
    mybot = Updater(settings.API_KEY, use_context=True)
    dp = mybot.dispatcher

    anketa_a = ConversationHandler(
      entry_points = [
        MessageHandler(Filters.regex('^(Стажер)$'), anketa_start)
      ],
      states = {
        "name": [MessageHandler(Filters.text, anketa_name)],
        "city": [MessageHandler(Filters.text, anketa_city)],
        "role": [MessageHandler(Filters.text, anketa_role)],
        "exp_role": [MessageHandler(Filters.regex('^(1|2|3|4|5)$'), anketa_exp_role)],
        "tuition": [MessageHandler(Filters.text, anketa_tuition)],
        "previous_exp": [MessageHandler(Filters.text, anketa_previous_exp)],
        "superpower": [MessageHandler(Filters.text, anketa_superpower)],
        "purpose": [MessageHandler(Filters.text, anketa_purpose)],
        "time_work": [MessageHandler(Filters.text, anketa_time_work)],
        "worth": [MessageHandler(Filters.text, anketa_worth)],
        "mail": [MessageHandler(Filters.text, anketa_mail)],
        "contacts": [
        CommandHandler("skip", anketa_own_skip),
        MessageHandler(Filters.text, anketa_contacts_end)
      ]
      },
      fallbacks = [
               CommandHandler("restart", cancel),
               MessageHandler(Filters.text | Filters.video | Filters.photo | Filters.document | Filters.location, anketa_dontknow)
      ] 
      )
    
    anketa_b = ConversationHandler(
      entry_points = [
        MessageHandler(Filters.regex('^(Владелец продукта)$'), anketa_start_own)
      ],
      states = {
        "name": [MessageHandler(Filters.text, anketa_own_name)],
        "city": [MessageHandler(Filters.text, anketa_own_city)],
        "project_name": [MessageHandler(Filters.text, anketa_own_project_name)],
        "working_condition": [MessageHandler(Filters.text, anketa_own_working_condition)],
        "mvp": [MessageHandler(Filters.text, anketa_own_mvp)],
        "presentation":[MessageHandler(Filters.text, anketa_own_presentation)],
        "team":[MessageHandler(Filters.text, anketa_own_team)],
        "mentor":[MessageHandler(Filters.text, anketa_own_mentor)],
        "own_mail":[MessageHandler(Filters.text, anketa_own_mail)],
        "own_contacts": [
        CommandHandler("skip", anketa_own_skip),
        MessageHandler(Filters.text, anketa_contacts_end)
      ]
      },
      fallbacks = [
              #  MessageHandler(Filters.command, cancel),
               MessageHandler(Filters.text | Filters.video | Filters.photo | Filters.document | Filters.location, anketa_dontknow)
      ] 
      )
    
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('admin', admin_bot))
    dp.add_handler(anketa_a)
    dp.add_handler(anketa_b)

    logging.info("Бот стартовал")
    mybot.start_polling()
    mybot.idle()

if __name__ == "__main__":
     main()
