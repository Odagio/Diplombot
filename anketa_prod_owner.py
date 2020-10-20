from telegram import ParseMode, ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler
from db import db, get_or_create_own, save_own_anketa
from utils import main_keyboard


def anketa_start_own(update, context):
    update.message.reply_text(
        """Привет! Я бот. Чтобы я мог найти для тебя команду, мне нужно собрать информацию.
Напиши свое имя и фамилию!""",
        reply_mark=ReplyKeyboardRemove()
    )
    return "name"


def anketa_own_name(update, context):
    user_name = update.message.text
    if len(user_name.split()) < 2:
        update.message.reply_text("Пожалуйста введите имя и фамилию")
        return "name"
    else:
        context.user_data["anketa"] = {"name": user_name}
        update.message.reply_text(
            "Из какого ты города?"
        )
        return "city"


def anketa_own_city(update, context):
    context.user_data["anketa"]["city"] = update.message.text
    update.message.reply_text(
            "Как называется твой проект? ?"
        )
    return "project_name"


def anketa_own_project_name(update, context):
    context.user_data["anketa"]["project_name"] = update.message.text
    reply_keyboard = [["платно", "бесплатно", "другое"]]
    update.message.reply_text("""Скажи, на каких условиях 
                              ты планируешь работать с командой? """,
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard,
                              one_time_keyboard=True, resize_keyboard=True)
                              )
    return "working_condition"


def anketa_own_working_condition(update, context):
    '''функция принимает ответ на вопрос о условиях, если пользователем выбран ответ другое, 
    то бот просит написать их вручную. и возвращает ответ опять, если выбраны другие кнопки(платно или бесплатно)
    то задает следующий вопрос'''
    work_cond = update.message.text
    if work_cond == "другое":
        update.message.reply_text("Напишите условия")
        return "working_condition"
    else:    
        context.user_data["anketa"] = {"working_condition": work_cond}
        reply_keyboard = [["да", "нет"]]
        update.message.reply_text("MVP или что-то, что уже есть?",
                                  reply_markup=ReplyKeyboardMarkup(reply_keyboard,
                                  one_time_keyboard=True, resize_keyboard=True)
        )
        return "mvp"
    

def anketa_own_mvp(update, context):
    """Функция принимает ответ на вопрос наличия MVP, если пользователь ответить утвердительно, то бот 
    попросит дать ссылку"""
    present = update.message.text
    if present == "да":
        update.message.reply_text("Скинь ссылку на проект")
        return "mvp"
    else:
        context.user_data["anketa"] = {"mvp": present}
        update.message.reply_text("Скинь ссылку на презентацию в Google Docs, чтоб мы могли показать её команде")
        return "presentation"


def anketa_own_presentation(update, context):
    context.user_data["anketa"]["presentation"] = update.message.text
    update.message.reply_text(
            "Кто тебе нужен в команду и почему?"
        )
    return "team"

def anketa_own_team(update, context):
    context.user_data["anketa"]["team"] = update.message.text
    update.message.reply_text(
            "Нужен ли тебе ментор/трекер проекта??"
        )
    return "mentor"


def anketa_own_mentor(update, context):
    context.user_data["anketa"]["mentor"] = update.message.text
    update.message.reply_text(
            """Спасибо за предоставленную информацию. По ходу набора группы я буду держать тебя в курсе.
Оставьте свою почту"""
        )
    return "own_mail"

def anketa_own_mail(update, context):
    context.user_data["anketa"]["own_mail"] = update.message.text
    update.message.reply_text(
        """Оставьте свой номер телефон или
         пропустите этот шаг, введя /skip"""
    )
    return "own_contacts"


def anketa_own_contacts_end(update, context):
    """ю"""
    context.user_data['anketa']['own_contacts'] = update.message.text
    user = get_or_create_own(db, update.effective_user,
                              update.message.chat_id)
    save_own_anketa(db, user['user_id'], context.user_data['anketa'])
    user_text = format_anketa(context.user_data['anketa'])
    update.message.reply_text(user_text, reply_markup=main_keyboard(),
                              parse_mode=ParseMode.HTML)
    return ConversationHandler.END


def anketa_own_skip(update, context):
    user = get_or_create_own(db, update.effective_user,
                              update.message.chat_id)
    save_own_anketa(db, user['user_id'], context.user_data['anketa'])
    user_text = format_anketa(context.user_data['anketa'])
    update.message.reply_text(user_text, reply_markup=main_keyboard(),
                              parse_mode=ParseMode.HTML)
    return ConversationHandler.END


def format_anketa(anketa):
    user_text = f"""<b>Имя Фамилия:</b> {anketa['name']}
<b>Оценка:</b> {anketa['city']}"""
    if anketa.get('contacts'):
        user_text += f"\n<b>Комментарий:</b> {anketa['contacts']}"
    return user_text


def anketa_dontknow(update, context):
    update.message.reply_text("я вас не понимаю")



# def cancel_own(update, context):
#     """ Cancel current conversation """
#     update.message.reply_text('Conversation ended')
#     return ConversationHandler.END