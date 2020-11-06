from db import db, get_or_create_own,  get_or_create_user, find_all_users, get_subscribed


# def admin_text (update, context):
#     print ('кто то зашел в прихожую')
#     find_us = find_all_users(db, update.effective_user,
#                               update.message.chat.id)
                              
#     print (find_us, type(find_us))      
#     uer_list = ""
#     for item in find_us:
#         uer_list = uer_list + "\n" + item.get('first_name')                      
#     update.message.reply_text(uer_list)
    
#     '''функция обращается в монго и показывает список юзеров, в последствии дает возможность написать им'''


def send_updates(update, context):
    admin_text = update.message.text
    for user in get_subscribed(db):
        context.bot.send_message(chat_id=user['chat_id'], text=f'Привет{admin_text}!')  


# [
#     {'_id': ObjectId('5f818b652d94d0e42a285b64'), 'user_id': 253662502, 'first_name': 'Vectormars', 'last_name': None, 'username': 'Vectormars', 'chat_id': 253662502, 'status': 'start'}, 
#     {'_id': ObjectId('5f9d3c0a5528c2a9883159a4'), 'user_id': 548824279, 'first_name': 'VK-innovation', 'last_name': None, 'username': 'Odagios', 'chat_id': 548824279, 'status': 'start'}
# ]
    

                           