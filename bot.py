from anketa_applicant import (anketa_start, anketa_name, anketa_city, anketa_mail, anketa_role, anketa_exp_role,
                              anketa_tuition,anketa_previous_exp, anketa_superpower, anketa_purpose, anketa_time_work,
                             anketa_working_condition, anketa_dontknow)
from anketa_prod_owner import (anketa_start_own, anketa_own_name, anketa_own_city,anketa_own_mail, anketa_own_project_name,
                               anketa_own_working_condition, anketa_own_mvp, anketa_own_presentation, anketa_own_team,
                               anketa_own_mentor)
from db import db, get_or_create_user, save_anketa, save_own_anketa, get_or_create_own
from handlers import greet_user, subscribe, unsubscribe, own_subscribe, own_unsubscribe
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler,ConversationHandler, Filters
import settings
from admin_handler import  admin_start, send_to_application, send_to_owns, admin_text_for_app, admin_text_for_own


logging.basicConfig(filename='bot.log', level=logging.INFO)


def main():
    mybot = Updater(settings.API_KEY, use_context=True)

    dp = mybot.dispatcher

    bot_send_messages = ConversationHandler(
      entry_points = [
        CommandHandler('superadmin', admin_start)
      ],
      states = {
        'choice':[ 
         CommandHandler('applicants', send_to_application),
         CommandHandler('owns', send_to_owns)
         ],
        'text_for_app': [MessageHandler(Filters.text, admin_text_for_app)],
        'text_for_own': [MessageHandler(Filters.text, admin_text_for_own)]
      },
      fallbacks = [
              
               MessageHandler(Filters.text | Filters.video | Filters.photo | Filters.document | Filters.location, anketa_dontknow)
      ] 
      )


    anketa_a = ConversationHandler(
      entry_points = [
        MessageHandler(Filters.regex('^(Стажер)$'), anketa_start)
      ],
      states = {
        "name": [MessageHandler(Filters.text, anketa_name)],
        "city": [MessageHandler(Filters.text, anketa_city)],
        "mail": [MessageHandler(Filters.text, anketa_mail)],
        "role": [MessageHandler(Filters.text, anketa_role)],
        "exp_role": [MessageHandler(Filters.text, anketa_exp_role)],
        "tuition": [MessageHandler(Filters.text, anketa_tuition)],
        "previous_exp": [MessageHandler(Filters.text, anketa_previous_exp)],
        "superpower": [MessageHandler(Filters.text, anketa_superpower)],
        "purpose": [MessageHandler(Filters.text, anketa_purpose)],
        "working_condition": [MessageHandler(Filters.text, anketa_working_condition)],
        "time_work": [MessageHandler(Filters.text, anketa_time_work)],
      },
      fallbacks = [
               MessageHandler(Filters.text | Filters.video | Filters.photo | Filters.document | Filters.location, anketa_dontknow)
      ] 
      )
    

    anketa_b = ConversationHandler(
      entry_points = [
        MessageHandler(Filters.regex('^(У меня есть продукт)$'), anketa_start_own)
      ],
      states = {
        "name_own": [MessageHandler(Filters.text, anketa_own_name)],
        "city_own": [MessageHandler(Filters.text, anketa_own_city)],
        "own_mail":[MessageHandler(Filters.text, anketa_own_mail)],
        "project_name_own": [MessageHandler(Filters.text, anketa_own_project_name)],
        "working_condition_own": [MessageHandler(Filters.text, anketa_own_working_condition)],
        "mvp_own": [MessageHandler(Filters.text, anketa_own_mvp)],
        "presentation_own":[MessageHandler(Filters.text, anketa_own_presentation)],
        "team_own":[MessageHandler(Filters.text, anketa_own_team)],
        "mentor_own":[MessageHandler(Filters.text, anketa_own_mentor)],
      },
      fallbacks = [          
               MessageHandler(Filters.text | Filters.video | Filters.photo | Filters.document | Filters.location, anketa_dontknow)
      ] 
      )
    
    
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('subscribe', subscribe))
    dp.add_handler(CommandHandler('unsubscribe', unsubscribe))
    dp.add_handler(CommandHandler('subscribe_me', own_subscribe ))
    dp.add_handler(CommandHandler('unsubscribe_me', own_unsubscribe))
    dp.add_handler(anketa_a)
    dp.add_handler(anketa_b)
    dp.add_handler(bot_send_messages)

    logging.info("Бот стартовал")
    mybot.start_polling()
    mybot.idle()

if __name__ == "__main__":
     main()
