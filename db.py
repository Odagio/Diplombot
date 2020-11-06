from datetime import datetime
from pymongo import MongoClient
import settings
client = MongoClient(settings.MONGO_LINK)

db = client[settings.MONGO_DB]


def chek_admin(db, effective_user,chat_id):
    user = db.admin_bot.find_one({"chat_id": chat_id})
    return user


def find_all_users (db, effective_user,chat_id):
    user_find = db.users.find({})
    usersid=[]
    for user in user_find:
        usersid.append(user)
    print (usersid)
    return usersid


def get_or_create_user(db, effective_user, chat_id):
    user = db.users.find_one({"user_id":effective_user.id})
    if not user:
        user = {
            "user_id":effective_user.id,
            "first_name": effective_user.first_name,
            "last_name": effective_user.last_name,
            "username": effective_user.username,
            "chat_id": chat_id,
            "status": "start"            
        }
        db.users.insert_one(user)
    return user


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


def get_or_create_own(db, effective_user, chat_id):
    user = db.own.find_one({"user_id":effective_user.id})
    if not user:
        user = {
            "user_id":effective_user.id,
            "first_name": effective_user.first_name,
            "last_name": effective_user.last_name,
            "username": effective_user.username,
            "chat_id": chat_id,
            "status": "start"            
        }
        db.own.insert_one(user)
    return user


def save_own_anketa(db, user_id, anketa_data):
    user = db.own.find_one({"user_id": user_id})
    anketa_data['created'] = datetime.now()
    if not 'anketa' in user:
        db.own.update_one(
            {'_id': user['_id']},
            {'$set': {'anketa': [anketa_data]}}
        )
    else:
        db.own.update_one(
            {'_id': user['_id']},
            {'$push': {'anketa': anketa_data}}
        )


def subscribe_user(db, user_data):
    if not user_data.get('subscribed'):
        db.users.update_one(
            {'_id': user_data['_id']},
            {'$set': {'subscribed': True}}
        )        


def unsubscribe_user(db, user_data):
            db.users.update_one(
            {'_id': user_data['_id']},
            {'$set': {'subscribed': False}}
        )        


def get_subscribed(db):
    return db.users.find({'subscribed': True})


def subscribe_own_db(db, user_data):
    if not user_data.get('subscribed'):
        db.own.update_one(
            {'_id': user_data['_id']},
            {'$set': {'subscribed': True}}
        )


def unsubscribe_own_db(db, user_data):
            db.own.update_one(
            {'_id': user_data['_id']},
            {'$set': {'subscribed': False}}
        )


def get_subscribed_own(db):
    return db.own.find({'subscribed': True})
       