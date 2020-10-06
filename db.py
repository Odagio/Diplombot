from datetime import datetime
from pymongo import MongoClient
import settings
client = MongoClient(settings.MONGO_LINK)

db = client[settings.MONGO_DB]

def get_or_create_user(db, effective_user, chat_id):
    user = db.users.find_one({"user_id":effective_user.id})
    if not user:
        user = {
            "user_id":effective_user.id,
            "first_name":effective_user.first_name,
            "last_name":effective_user.last_name,
            "username":effective_user.username,
            "chat_id":chat_id,
            "status": "start"            
        }
        db.users.insert_one(user)
    return user


def change_status(user, new_status):
    # user = db.users.find_one({"user_id": user_id})
    db.users.update_one(
            {'_id': user['_id']},
            {'$set': {'status': new_status}}
    )
    
    # if not 'status' in new_status:
    #     db.users.update_one(
    #         {'_id': user['_id']},
    #         {'$set': {'status': new_status}}
    #     )
    # else:
    #     db.users.update_one(
    #         {'_id': user['_id']},
    #         {'$push': {'status': new_status}}
    #     )

def save_anketa(db, user_id, anketa_data):
    user = db.users.find_one({"user_id": user_id})
    anketa_data['created'] = datetime.now()
    if not 'anketa' in user:
        db.users.update_one(
            {'_id': user['_id']},
            {'$set': {'anketa': [anketa_data]}}
        )
    else:
        db.users.update_one(
            {'_id': user['_id']},
            {'$push': {'anketa': anketa_data}}
        )