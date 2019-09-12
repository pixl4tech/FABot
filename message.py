from database import *
import common
import datetime

"""
Модуль функций возврата расписания в виде текстовых сообщений (telegram)
"""

def get_schedule(group_id=None, begin_dt=None, end_dt=None):
    """
    Возвращает расписание за конкретный период в одном сообщении

    :param group_id: ID группы
    :param begin_dt: Дата первого дня
    :param end_dt: Дата последнего дня
    :return: str
    """

    sch = common.Schedule(connection=Connection(), group_id=group_id, begin_dt=begin_dt, end_dt=end_dt)
    return sch.get_message()


def get_daily_schedule_list(group_id=None, begin_dt=None, end_dt=None):
    """
    Возвращает расписание за конкретный период набором сообщений по дням

    :param group_id: ID группы
    :param begin_dt: Дата первого дня
    :param end_dt: Дата последнего дня
    :return: list[str]

    """

    days_list = common.Schedule(connection=Connection(), group_id=group_id, begin_dt=begin_dt, end_dt=end_dt).days
    if len(days_list) > 0:
        message_list = []
        for day in days_list:
            for day_mess in day.get_message():
                message_list.append(day_mess)
        return message_list
    else:
        return ['Нет пар']


def get_schedule_by_day(group_id=None, date=None):
    """
    Возвращает расписание за конкретный день

    :param group_id: ID группы
    :param date: Дата
    :return: str

    """

    days_list = common.Schedule(connection=Connection(), group_id=group_id, begin_dt=date, end_dt=date).days
    if len(days_list) > 0:
        result = []
        for day in days_list:
            for day_item in day.get_message():
                result.append(day_item)
        return result
    else:
        return ['Нет пар']


def get_now(group_id=None, date=None):
    """
    Возвращает текущую пару
    :param group_id:
    :param date:
    :return:
    """

    date = date if date else datetime.date.today().isoformat()
    days = common.Schedule(connection=Connection(), group_id=group_id, begin_dt=date, end_dt=date).days
    if len(days) > 0:
        day = days[0]
        now = datetime.datetime.now().time()
        for cls in day.classes:
            if cls.time_start > now or cls.time_end > now:
                return '{0}\n-----------------------------\n{1}'.format(day.date, str(cls.get_message()))

        return 'Пар нет'

    else:
        return 'Пар нет'


def get_exams(group_id=None):
    days_list = common.Schedule(connection=Connection(), group_id=group_id,
                                begin_dt=datetime.datetime.strptime(str(datetime.date.today()), '%Y-%m-%d'),
                                end_dt=config.END_DT, exam_flg=True).days

    if len(days_list) > 0:
        message = []
        for day in days_list:
            for day_item in day.get_message():
                message.append(day_item)
        return message
    else:
        return ['Информация о зачетах и экзаменах не найдена.']

