from db import db, get_or_create_user, save_anketa
from telegram import ParseMode, ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler
from utils import main_keyboard


def anketa_start(update, context):
    '''Функция открывает диалог, тут же записывает в mongo переменной user в коллекцию users'''
    user = get_or_create_user(db, update.effective_user,
                              update.message.chat.id)
    update.message.reply_text(
        """Привет! Чтобы я мог найти для тебя команду, мне нужно собрать немного информации о тебе.
Напиши свое имя и фамилию!""",
        reply_mark=ReplyKeyboardRemove()
    )
    return "name"


def anketa_name(update, context):
    user_name = update.message.text
    if len(user_name.split()) < 2:
        update.message.reply_text("Пожалуйста введите имя и фамилию")
        return "name"
    else:
        '''здесь анкета переписывается, если введено имя не правильно'''
        context.user_data["anketa"] = {"name": user_name}
        update.message.reply_text(
            "Из какого ты города?"
        )
        return "city"


def anketa_city(update, context):
    context.user_data["anketa"]["city"] = update.message.text
    update.message.reply_text(
            "Расскажи, какую роль в проекте ты бы взял на себя?"
        )
    return "role"


def anketa_role(update, context):
    context.user_data["anketa"]["role"] = update.message.text
    reply_keyboard = [["1", "2", "3", "4", "5"]]
    update.message.reply_text(
            "Расскажи, какой опыт у тебя в этой роли?",
             reply_markup=ReplyKeyboardMarkup(reply_keyboard,
                one_time_keyboard=True, resize_keyboard=True)
            )
    return "exp_role"


def anketa_exp_role(update, context):
    context.user_data["anketa"]["exp_role"] = update.message.text
    update.message.reply_text(
            "как ты обучался этому?"
        )
    return "tuition"


def anketa_tuition(update, context):
    context.user_data["anketa"]["tuition"] = update.message.text
    update.message.reply_text(
            "Расскажи коротко о своём прежнем опыте. 2-3 предложения.?"
        )
    return "previous_exp"


def anketa_previous_exp(update, context):
    context.user_data["anketa"]["previous_exp"] = update.message.text
    update.message.reply_text(
            "Расскажи, какая у тебя есть суперспособность? Твоя наиболее сильная сторона."
        )
    return "superpower"


def anketa_superpower(update, context):
    context.user_data["anketa"]["superpower"] = update.message.text
    update.message.reply_text(
            "Что бы ты хотел получить от работы на проекте?"
        )
    return "purpose"

    
def anketa_purpose(update, context):
    context.user_data["anketa"]["purpose"] = update.message.text
    update.message.reply_text(
            "Расскажи сколько свободного времени в неделю ты бы мог выделить для проекта?"
        )
    return "time_work"

    
def anketa_time_work(update, context):
    context.user_data["anketa"]["time_work"] = update.message.text
    update.message.reply_text(
            "Что для тебя важно на проекте?"
        )
    return "worth"    


def anketa_worth(update, context):
    context.user_data["anketa"]["worth"] = update.message.text
    update.message.reply_text(
             """
Оставьте свою почту"""
        )
    return "mail"    


def anketa_mail(update, context):
    context.user_data["anketa"]["mail"] = update.message.text
    update.message.reply_text(
        """Оставьте свой номер телефон или
пропустите этот шаг, введя /skip"""
    )
    return "contacts"


def anketa_contacts_end(update, context):
    '''анкета принимает на вход контакты и записывает в монго все данные'''
    context.user_data['anketa']['contacts'] = update.message.text
    user = get_or_create_user(db, update.effective_user,
                              update.message.chat_id)
    save_anketa(db, user['user_id'], context.user_data['anketa'])
    user_text = format_anketa(context.user_data['anketa'])
    update.message.reply_text(user_text, reply_markup=main_keyboard(),
                              parse_mode=ParseMode.HTML)
    return ConversationHandler.END


def anketa_skip(update, context):
    user = get_or_create_user(db, update.effective_user,
                              update.message.chat_id)
    save_anketa(db, user['user_id'], context.user_data['anketa'])
    user_text = format_anketa(context.user_data['anketa'])
    update.message.reply_text(user_text, reply_markup=main_keyboard(),
                              parse_mode=ParseMode.HTML)
    return ConversationHandler.END


def format_anketa(anketa):
    user_text = f"""Мы записали анкету, если есть ошибка в данных, то пройдите ее еще раз.
\n
<b>чтобы получать презентации проектов, набери комманду /subscribe, если хочешь отписаться то /unsbscribe:</b>
\n
<b>имя фамилия:</b> {anketa['name']}
<b>город:</b> {anketa['city']}
<b>роль в проекте:</b> {anketa['role']}
<b>опыт:</b> {anketa['exp_role']}
<b>обучение:</b> {anketa['tuition']}
<b>предыдущий опыт:</b> {anketa['previous_exp']}
<b>супер сила:</b> {anketa['superpower']}
<b>получение от проекта:</b> {anketa['purpose']}
<b>время работы:</b> {anketa['time_work']}
<b>важность в проекте:</b> {anketa['worth']}
<b>почта:</b> {anketa['mail']}
<b>Спасибо за предоставленную информацию. 
"""
    if anketa.get('contacts'):
        user_text += f"<b>телефон:</b> {anketa['contacts']}"
    return user_text


def anketa_dontknow(update, context):
    update.message.reply_text("я вас не понимаю")
