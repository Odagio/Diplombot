from telegram import ReplyKeyboardMarkup, KeyboardButton
import settings


def main_keyboard():
    return ReplyKeyboardMarkup([
          ['Стажер', 'Владелец продукта']
          ], one_time_keyboard=True, resize_keyboard=True)


def admin_keyboard():
    return ReplyKeyboardMarkup([
          ['/owns', '/applicants']
          ], one_time_keyboard=True, resize_keyboard=True)
