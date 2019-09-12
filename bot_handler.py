import telebot
from telebot import types
import message as sch
import datetime
import common
import threading
from database import *

# bot init
bot = telebot.TeleBot(config.TELEGRAM_API)


# Обычный режим
def create_markup():
    markup = types.ReplyKeyboardMarkup(row_width=3)
    itembtn2 = types.KeyboardButton('Сегодня')
    itembtn5 = types.KeyboardButton('Завтра')
    itembtn6 = types.KeyboardButton('Эта неделя')
    itembtn7 = types.KeyboardButton('След. неделя')
    itembtn3 = types.KeyboardButton('Меню')
    itembtn4 = types.KeyboardButton('Группа')
    itembtn8 = types.KeyboardButton('О боте')
    itembtn9 = types.KeyboardButton('Факультет')
    itembtn10 = types.KeyboardButton('Экзамены')
    markup.add(itembtn3, itembtn2, itembtn5, itembtn6, itembtn7, itembtn9, itembtn4, itembtn8, itembtn10)
    return markup


def validate_date(date=None):
    try:
        target_day = date + '.{0}'.format(str(datetime.date.today().year))
        req_date = datetime.datetime.strptime(target_day, '%d.%m.%Y')
    except:
        target_day = date
        try:
            req_date = datetime.datetime.strptime(target_day, '%d.%m.%Y')
        except:
            try:
                req_date = datetime.datetime.strptime(target_day, '%d.%m.%y')
            except:
                req_date = 'err'
    return req_date


@bot.message_handler(commands=['send'])
def send_text(message):
    if str(message.chat.id) == config.ADMIN_USER_ID:
        users = common.get_users_list()
        mess = message.text.replace('/send','')
        if mess == '':
            pass
        for u in users:
            try:
                print('user {0}'.format(u))
                bot.send_message(chat_id=u, text=mess)
            except:
                continue


@bot.message_handler(commands=['menu'])
def menu_text(message, params=None):
    inline_mode = True if params is not None else False
    conn = Connection()
    user = common.User(user=message.chat, connection=conn)
    group_id = user.get_group_id()
    if group_id:
        keyboard = types.InlineKeyboardMarkup()
        callback_button = types.InlineKeyboardButton(text="Расписание на сегодня", callback_data="Сегодня")
        keyboard.add(callback_button)
        callback_button = types.InlineKeyboardButton(text="Расписание на завтра", callback_data="Завтра")
        keyboard.add(callback_button)
        callback_button = types.InlineKeyboardButton(text="Расписание экзаменов", callback_data="Экзамены")
        keyboard.add(callback_button)
        callback_button = types.InlineKeyboardButton(text="Настройки", callback_data="Настройки")
        keyboard.add(callback_button)
        callback_button = types.InlineKeyboardButton(text="Статистика бота", callback_data="Статистика")
        keyboard.add(callback_button)
        callback_button = types.InlineKeyboardButton(text="О боте", callback_data="О боте")
        keyboard.add(callback_button)
        markup = create_markup()
        bot.send_message(message.chat.id, "Бот-расписание", reply_markup=markup)
        bot.send_message(message.chat.id, "Меню [{0}]:".format(user.get_group()), reply_markup=keyboard)
    else:
        markup = types.ForceReply(selective=False)
        bot.send_message(message.chat.id, "Введите свою группу, например: ПИ1-1", reply_markup=markup)


@bot.message_handler(commands=['now'])
def now_text(message, params=None):
    inline_mode = True if params is not None else False
    user = common.User(user=message.chat)
    group_id = user.get_group_id()
    markup = create_markup()
    if group_id:
        bot.send_message(message.chat.id, sch.get_now(group_id), reply_markup=markup)
    else:
        markup = types.ForceReply(selective=False)
        bot.send_message(message.chat.id, "Введите свою группу, например: ПИ1-1", reply_markup=markup)


@bot.message_handler(commands=['today'])
def today_text(message, params=None):
    inline_mode = True if params is not None else False
    conn = Connection()
    user = common.User(user=message.chat, connection=conn)
    group_id = user.get_group_id()
    markup = create_markup()
    if group_id:
        today = datetime.datetime.now().date().isoformat()
        for mess in sch.get_schedule_by_day(group_id, today):
            bot.send_message(message.chat.id, mess, reply_markup=markup, parse_mode='html')
    else:
        markup = types.ForceReply(selective=False)
        bot.send_message(message.chat.id, "Введите свою группу, например: ПИ1-1", reply_markup=markup)


@bot.message_handler(commands=['setting'])
def setting_text(message, params=None):
    inline_mode = True if params is not None else False
    conn = Connection()
    user = common.User(user=message.chat, connection=conn)
    group_id = user.get_group_id()
    markup = create_markup()
    if group_id:
        bot.send_message(message.chat.id, """/group - Сменить группу,\n /fac - Сменить факультет""", reply_markup=markup)
    else:
        markup = types.ForceReply(selective=False)
        bot.send_message(message.chat.id, "Введите свою группу, например: ПИ1-1", reply_markup=markup)


@bot.message_handler(commands=['tomorrow'])
def next_text(message, params=None):
    inline_mode = True if params is not None else False
    conn = Connection()
    user = common.User(user=message.chat, connection=conn)
    group_id = user.get_group_id()
    if group_id:
        nextday = (datetime.datetime.now() + datetime.timedelta(days=1)).date().isoformat()
        markup = create_markup()
        for mess in sch.get_schedule_by_day(group_id, nextday):
            bot.send_message(message.chat.id, mess, reply_markup=markup, parse_mode='html')
    else:
        markup = types.ForceReply(selective=False)
        bot.send_message(message.chat.id, "Введите свою группу, например: ПИ1-1", reply_markup=markup)


@bot.message_handler(commands=['help'])
def help_text(message, params=None):
    inline_mode = True if params is not None else False
    text = """
    Для начала необходимо указать свою группу, например: ПИ4-1.\n
    Список команд:\n
    /today - Сегодня\n
    /tomorrow - Завтра\n
    /week - На неделю\n
    /2week - На след. неделю\n
    /group - Поменять группу\n
    /fac - Поменять факультет\n
    /help - Справка\n
    /menu - Меню\n
    /about - О боте
    """
    markup = create_markup()
    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.message_handler(commands=['week'])
def week_text(message, params=None):
    inline_mode = True if params is not None else False
    conn = Connection()
    user = common.User(user=message.chat, connection=conn)
    group_id = user.get_group_id()
    if group_id:
        today = datetime.datetime.strptime(params[1], '%Y-%m-%d') if inline_mode and len(params) == 2 else \
                                           datetime.datetime.strptime(str(datetime.date.today()), '%Y-%m-%d')
        date1 = today - datetime.timedelta(days=today.weekday())
        date2 = date1 + datetime.timedelta(days=5)
        markup = create_markup()
        bot.send_message(message.chat.id, "За неделю", reply_markup=markup)
        callback_dt = date2 + datetime.timedelta(days=3)
        keyboard1 = types.InlineKeyboardMarkup(row_width=2)
        callback_button1 = types.InlineKeyboardButton(text="Далее »", callback_data="Эта неделя__{0}".format(
            str(callback_dt.date())))
        callback_button2 = types.InlineKeyboardButton(text="« Назад", callback_data="Эта неделя__{0}".format(
            str((callback_dt - datetime.timedelta(days=14)).date())))
        keyboard1.add(callback_button2, callback_button1)
        mess_list = sch.get_daily_schedule_list(group_id, date1, date2)
        for mess in mess_list:
            bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=keyboard1 if mess == mess_list[-1] else None)
    else:
        markup = types.ForceReply(selective=False)
        bot.send_message(message.chat.id, "Введите свою группу, например: ПИ1-1", reply_markup=markup)


@bot.message_handler(commands=['2week'])
def twoweek_text(message, params=None):
    inline_mode = True if params is not None else False
    conn = Connection()
    user = common.User(user=message.chat, connection=conn)
    group_id = user.get_group_id()
    if group_id:
        today = datetime.datetime.strptime(params[1], '%Y-%m-%d') if inline_mode and len(params) == 2 else \
                                           datetime.datetime.strptime(str(datetime.date.today()), '%Y-%m-%d')
        date1 = today - datetime.timedelta(days=today.weekday()) + datetime.timedelta(days=7)
        date2 = date1 + datetime.timedelta(days=5)
        markup = create_markup()
        bot.send_message(message.chat.id, "На след. неделю", reply_markup=markup)
        callback_dt = date2 + datetime.timedelta(days=3)
        keyboard1 = types.InlineKeyboardMarkup(row_width=2)
        callback_button1 = types.InlineKeyboardButton(text="Далее »", callback_data="Эта неделя__{0}".format(
            str(callback_dt.date())))
        callback_button2 = types.InlineKeyboardButton(text="« Назад", callback_data="Эта неделя__{0}".format(
            str((callback_dt - datetime.timedelta(days=14)).date())))
        keyboard1.add(callback_button2, callback_button1)
        mess_list = sch.get_daily_schedule_list(group_id, date1, date2)
        for mess in mess_list:
            bot.send_message(message.chat.id, mess, parse_mode='html',
                             reply_markup=keyboard1 if mess == mess_list[-1] else None)
    else:
        markup = types.ForceReply(selective=False)
        bot.send_message(message.chat.id, "Введите свою группу, например: ПИ1-1", reply_markup=markup)


@bot.message_handler(commands=['exam'])
def exam_text(message, params=None):
    inline_mode = True if params is not None else False
    conn = Connection()
    user = common.User(user=message.chat, connection=conn)
    group_id = user.get_group_id()
    if group_id:
        mess_list = sch.get_exams(group_id)
        markup = create_markup()
        bot.send_message(message.chat.id, "Расписание экзаменов:", reply_markup=markup, parse_mode='html')
        for mess in mess_list:
            bot.send_message(message.chat.id, mess, parse_mode='html')
    else:
        markup = types.ForceReply(selective=False)
        bot.send_message(message.chat.id, "Введите свою группу, например: ПИ1-1", reply_markup=markup, parse_mode='html')


@bot.message_handler(commands=['stat'])
def stat_text(message, params=None):
    inline_mode = True if params is not None else False
    conn = Connection()
    user = common.User(user=message.chat, connection=conn)
    group_id = user.get_group_id()
    markup = create_markup()
    if inline_mode and len(params) == 2 and str(message.chat.id) == config.ADMIN_USER_ID:
        if params[1] == 'Лог':
            log = sch.get_stat_requests(str(message.chat.id))
            for mess in log:
                bot.send_message(message.chat.id, mess, reply_markup=markup)
        elif params[1] == 'Фак':
            log = sch.get_stat_fac()
            for mess in log:
                bot.send_message(message.chat.id, mess, reply_markup=markup, parse_mode='html')
    else:
        if group_id:
            bot.send_message(message.chat.id,
                             sch.get_statistics(str(message.chat.id)), reply_markup=markup)
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            callback_button = types.InlineKeyboardButton(text="По факультетам", callback_data="Статистика__Фак")
            keyboard.add(callback_button)
            if str(message.chat.id) == config.ADMIN_USER_ID:
                callback_button = types.InlineKeyboardButton(text="Лог запросов", callback_data="Статистика__Лог")
                keyboard.add(callback_button)
            bot.send_message(message.chat.id, "Функции статистики", reply_markup=keyboard)
        else:
            markup = types.ForceReply(selective=False)
            bot.send_message(message.chat.id, "Введите свою группу, например: ПИ1-1", reply_markup=markup)




@bot.message_handler(commands=['about'])
def about_text(message, params=None):
    inline_mode = True if params is not None else False
    conn = Connection()
    user = common.User(user=message.chat, connection=conn)
    group_id = user.get_group_id()
    markup = create_markup()
    if group_id:
        date = user.find_snap_date()
        bot.send_message(message.chat.id,
                         """Бот показывает расписание для групп Финансового Университета.\n\nВерсия: 1.2.1\nДата обновления расписания: {0}\nСообщить о багах, предложениях можно сюда: @pushwork""".format(
                             date
                         ), reply_markup=markup)
        bot.send_message(message.chat.id, 'Наш бот в VK: https://vk.com/bot_fu \nПодписывайся {0}'.format(
            config.EMODJI.get('like')))
    else:
        markup = types.ForceReply(selective=False)
        bot.send_message(message.chat.id, "Введите свою группу, например: ПИ1-1", reply_markup=markup)


@bot.message_handler(commands=['group', 'g'])
def group_text(message, params=None):
    inline_mode = True if params is not None else False
    markup = types.ForceReply(selective=False)
    user = common.User(user=message.chat, connection=Connection())
    if inline_mode and len(params) == 2:
        group = user.find_group(params[1])
        if len(group) > 0:
            if user.group_id and user.group_id != group[0]:
                user.set_add_group(group_id=user.group_id)
            user.set_group(group_id=group[0], group_name=group[1])
            markup = create_markup()
            bot.send_message(message.chat.id,
                             'Ваша группа {0} сохранена. Поменять ее можно в меню или выбрав команду /group'.format(
                                 user.group_name),reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'Ошибка! указанная группа не найдена.')
            markup = types.ForceReply(selective=False)
            bot.send_message(message.chat.id, "Введите свою группу, например: ПИ1-1", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Введите свою группу, например: ПИ1-1", reply_markup=markup)
        if user.get_group():
            keyboard1 = types.InlineKeyboardMarkup(row_width=2)
            callback_button1 = types.InlineKeyboardButton(text="{0}".format(user.get_group()),
                                                          callback_data="Группа__{0}".format(user.get_group()))
            keyboard1.add(callback_button1)
            if user.add_group_id:
                group_nm = user.get_add_group()
                callback_button2 = types.InlineKeyboardButton(text="{0}".format(group_nm),
                                                          callback_data="Группа__{0}".format(group_nm))
                keyboard1.add(callback_button2)
            bot.send_message(message.chat.id, "Ранее вводили:", reply_markup=keyboard1)


@bot.message_handler(commands=['fac', 'start'])
def fac_text(message, params=None):
    inline_mode = True if params is not None else False
    user = common.User(user=message.chat, connection=Connection())
    if inline_mode and len(params) == 2:
        text = ', '.join([g.get('group_name') for g in user.get_groups_by_faculty(params[1])])
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
                              text=text if text else 'Нет данных')
        markup = types.ForceReply(selective=False)
        bot.send_message(message.chat.id, "Введите свою группу, например: ПИ1-1", reply_markup=markup)
    else:
        conn = Connection()
        user = common.User(user=message.chat, connection=conn)
        fac_list = user.show_faculty()
        keyboard = types.InlineKeyboardMarkup()
        for f in fac_list:
            keyboard.add(types.InlineKeyboardButton(text=str(f['faculty_desc']), callback_data="Факультет__{0}".format(f['faculty_id'])))
        bot.send_message(message.chat.id, "Выберите ваш факультет", reply_markup=keyboard)


bot_func = {
    'Сегодня': today_text,
    'Завтра': next_text,
    'Эта неделя': week_text,
    'След. неделя': twoweek_text,
    'Меню': menu_text,
    'Группа': group_text,
    'О боте': about_text,
    'Факультет': fac_text,
    'Экзамены': exam_text,
    'Статистика': stat_text,
    'Настройки': setting_text
}


@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.reply_to_message:
        if message.reply_to_message.text == 'Введите свою группу, например: ПИ1-1':
            conn = Connection()
            user = common.User(user=message.chat, connection=conn)
            group = user.find_group(message.text)
            if len(group) > 0:
                if user.group_id and user.group_id != group[0]:
                    user.set_add_group(group_id=user.group_id)
                user.set_group(group_id=group[0], group_name=group[1])
                bot.send_message(message.chat.id, 'Ваша группа {0} сохранена. Поменять ее можно в меню или выбрав команду /group'.format(
                    user.group_name))
                markup = create_markup()
                bot.send_message(message.chat.id, "Бот-расписание", reply_markup=markup)
                bot.send_message(message.chat.id, 'Наш бот в VK: https://vk.com/bot_fu \nПодписывайся {0}'.format(
                    config.EMODJI.get('like')))
            elif message.reply_to_message.text == 'Выберите ваш факультет':
                pass
            else:
                bot.send_message(message.chat.id, 'Ошибка! указанная группа не найдена.')
                markup = types.ForceReply(selective=False)
                bot.send_message(message.chat.id, "Введите свою группу, например: ПИ1-1", reply_markup=markup)
    elif bot_func.get(message.text):
        bot_func[message.text](message)
    else:
        dt = validate_date(message.text)
        if dt != 'err':
            conn = Connection()
            user = common.User(user=message.chat, connection=conn)
            group_id = user.get_group_id()
            if group_id:
                req_day = dt.date().isoformat()
                bot.send_message(message.chat.id, sch.get_schedule_by_day(group_id, req_day))
            else:
                markup = types.ForceReply(selective=False)
                bot.send_message(message.chat.id, "Введите свою группу, например: ПИ1-1", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'Ошибка ввода даты!\n Попробуй так: 5.9 или так: 05.09.2016')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        params_list = call.data.split('__') if call.data else None
        call_command = params_list[0] if params_list else None
        if bot_func.get(call_command):
            bot_func[call_command](call.message, params_list)


lock = threading.Lock()
