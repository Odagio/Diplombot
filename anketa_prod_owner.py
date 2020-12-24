from db import db, get_or_create_own, save_own_anketa, get_or_create_user
from telegram import ParseMode, ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler
from utils import main_keyboard
import gspread
import settings


def anketa_start_own(update, context):
    '''Функция открывает диалог, тут же записывает в mongo переменной user в коллекцию own'''
    user = get_or_create_own(db, update.effective_user,
                              update.message.chat.id)            
    update.message.reply_text(
        """Привет! Я бот. Чтобы я мог найти для тебя команду, мне нужно собрать информацию.
Напиши свое имя и фамилию!""",
        reply_mark=ReplyKeyboardRemove()
    )
    return "name_own"


def anketa_own_name(update, context):
    user_name = update.message.text
    if len(user_name.split()) < 2:
        update.message.reply_text("Пожалуйста введите имя и фамилию")
        return "name_own"
    else:
        '''context.user_data переписывает анкету, то есть заменяет то, что уже записано '''
        context.user_data["anketa"] = {"name_own": user_name}
        update.message.reply_text(
            "Из какого ты города?"
        )
        return "city_own"


def anketa_own_city(update, context):
    context.user_data["anketa"]["city_own"] = update.message.text
    update.message.reply_text(
            "Напиши свой e-mail для связи"
        )
    return "own_mail"

def anketa_own_mail(update, context):
    context.user_data["anketa"]["own_mail"] = update.message.text
    update.message.reply_text(
            """Как называется твой проект?"""
        )
    return "project_name_own"


def anketa_own_project_name(update, context):
    context.user_data["anketa"]["project_name_own"] = update.message.text
    reply_keyboard = [["платно", "бесплатно", "другие условия"]]
    update.message.reply_text("""Скажи, на каких условиях 
ты планируешь работать с командой? """,
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard,
                              one_time_keyboard=True, resize_keyboard=True)
                              )
    return "working_condition_own"


def anketa_own_working_condition(update, context):
    '''функция принимает ответ на вопрос о условиях, если пользователем выбран ответ другое, 
    то бот просит написать их вручную. и возвращает ответ опять, если выбраны другие кнопки(платно или бесплатно)
    то задает следующий вопрос'''
    work_cond = update.message.text
    if work_cond == "другие условия":
        update.message.reply_text("Напиши условия")
        return "working_condition_own"
    else:    
        context.user_data["anketa"]["working_condition_own"] = work_cond
        reply_keyboard = [["да", "нет"]]
        update.message.reply_text("MVP или что-то, уже есть?",
                                  reply_markup=ReplyKeyboardMarkup(reply_keyboard,
                                  one_time_keyboard=True, resize_keyboard=True)
        )
        return "mvp_own"
    

def anketa_own_mvp(update, context):
    '''Функция принимает ответ на вопрос наличия MVP, если пользователь ответить утвердительно, то бот 
    попросит дать ссылку'''
    present = update.message.text
    if present == "да":
        update.message.reply_text("Скинь ссылку на проект")
        return "mvp_own"
    else:
        context.user_data["anketa"]["mvp_own"] = present
        update.message.reply_text("Скинь ссылку на презентацию в Google Docs, чтоб мы могли показать её команде")
        return "presentation_own"


def anketa_own_presentation(update, context):
    context.user_data["anketa"]["presentation_own"] = update.message.text
    update.message.reply_text(
            "Кто тебе нужен в команду и почему?"
        )
    return "team_own"


def anketa_own_team(update, context):
    context.user_data["anketa"]["team_own"] = update.message.text
    reply_keyboard = [["да", "нет"]]
    update.message.reply_text(
            "Нужен ли тебе ментор/трекер проекта?",
                                  reply_markup=ReplyKeyboardMarkup(reply_keyboard,
                                  one_time_keyboard=True, resize_keyboard=True)
        )
    return "mentor_own"


def anketa_own_mentor(update, context):
    context.user_data["anketa"]["mentor_own"] = update.message.text
    user = get_or_create_own(db, update.effective_user,
                              update.message.chat_id)
    save_own_anketa(db, user['user_id'], context.user_data['anketa'])
    user_text_own = format_anketa_own(context.user_data['anketa'])
    update.message.reply_text(user_text_own, reply_markup=main_keyboard(),
                              parse_mode=ParseMode.HTML)
    #Записываем в гугл
    gc = gspread.service_account(filename= 'credentials.json')#отсылка на апи
    sh = gc.open_by_key(settings.SPREAD_SHEET_ID)#отсылка на лист
    worksheet = sh.get_worksheet (1)#отсылка на номер листа
    users = context.user_data['anketa']
    asd = list(users.values())#перевод словаря в список анкеты
    avd = list(user.values())#перевод словаря в список данных пользователя
    # print (avd[1:4])
    # print (asd[:-1])
    worksheet.append_row(avd[1:5] + asd[:-1])#Складывает и записывает списки именно те
    return ConversationHandler.END


def format_anketa_own(anketa):
    user_text_own = f"""Мы записали анкету, если есть ошибка в данных, то пройдите ее еще раз.
\n
<b>чтобы получать презентации проектов, набери комманду /subscribe_me, если хочешь отписаться то /unsbscribe_me:</b>
\n    
<b>имя фамилия:</b> {anketa['name_own']}
<b>город:</b> {anketa['city_own']}
<b>почта:</b> {anketa['own_mail']}
<b>название проекта:</b> {anketa['project_name_own']}
<b>условия работы:</b> {anketa['working_condition_own']}
<b>mvp:</b> {anketa['mvp_own']}
<b>презентация:</b> {anketa['presentation_own']}
<b>команда:</b> {anketa['team_own']}
<b>ментор:</b> {anketa['mentor_own']}
"""
    return user_text_own


def anketa_dontknow(update, context):
    update.message.reply_text("я вас не понимаю")
