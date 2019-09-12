import psycopg2.extras
from database import *
from config import *
from collections import OrderedDict


class Schedule:

    """
    Класс для формирования объектов расписания
    """

    def __init__(self, connection=Connection(), group_id=None, begin_dt=None, end_dt=None, exam_flg=False):
        snap_id = Query("""select snap_id
                              from "actual_snap"
                              where group_id = {group_id} 
                               """, connection).fetchall(group_id=group_id)
        snap_id = snap_id[0]['snap_id'] if snap_id else None

        self.begin_dt = begin_dt
        self.end_dt = end_dt
        row_list = Query(""" select s.*, t.time_number, t.time_start, t.time_end
                              from "schedule" s
                              left join "time_class" t on s.time_id = t.time_id
                              where snap_id = {snap_id} and group_id = {group_id} and (date >= '{begin_dt}' and 
                              date <= '{end_dt}' {exam_flt})
                              ORDER BY date, time_number
                               """, connection).fetchall(group_id=group_id, snap_id=snap_id,
                                                         begin_dt=begin_dt, end_dt=end_dt,
                                                         exam_flt=" and exam_flg = 'Y' " if exam_flg else "") \
                                                            if snap_id else []

        self.classes_list = []
        for row in row_list:
            self.classes_list.append(Class(row))

        _dates_dict = OrderedDict()
        for item in self.classes_list:
            _dates_dict.update({item.date: None})
        self.days = []
        for date in _dates_dict:
            list = []
            for item in self.classes_list:
                if item.date == date:
                    list.append(item)
            self.days.append(Day(date, list))

    def get_message(self):
        """
        Формирует сообщение(сообщения) с парами.
        :return: list
        """

        mess_list = []
        mess_txt = """*────────────────────\n{0} - {1}\n*────────────────────\n""".format(self.begin_dt.date(), self.end_dt.date())
        for item in self.days:
            for day_item in item.get_message():
                # 4096 макс. длина сообщения (4080, потому что 16 зарезервировано строкой в самом конце сообщения)
                if len(mess_txt + day_item) > 4080:
                    mess_list.append(mess_txt)
                    mess_txt = day_item
                else:
                    mess_txt += day_item
        # Добавляем завершающие 16 символов
        mess_txt += "\n*────────────────────"
        mess_list.append(mess_txt)
        return mess_list


class Day:

    """
    Класс для формирования объектов учебных дней
    """

    def __init__(self, date, class_list):
        '''
        
        :param date: date 
        :param class_list: list([class])
        '''

        self._wdays = (u'Понедельник', u'Вторник', u'Среда', u'Четверг', u'Пятница', u'Суббота', u'Воскресенье')
        self.weekday = self._wdays[date.weekday()]
        self.classes = class_list
        self.date = date

    def get_message(self):
        mess_list = []
        mess_txt = """\n<b>{2} {0}, {1}</b>\n────────────────────\n""".format(self.date.isoformat(), self.weekday,
                                                                                  EMODJI.get('open_book'))
        for item in self.classes:
            # 4096 макс. длина сообщения (4080, потому что 16 зарезервировано строкой в самом конце сообщения)
            if len(mess_txt + item.get_message()) > 4080:
                mess_list.append(mess_txt)
                mess_txt = item.get_message()
            else:
                mess_txt += item.get_message()
        # Добавляем завершающие 16 символов
        mess_txt += "────────────────────"
        mess_list.append(mess_txt)
        return mess_list


class Class:
    """
    Класс для формирования объектов занятий
    """

    def __init__(self, params=None):
        if isinstance(params, dict) or isinstance(params, psycopg2.extras.RealDictRow):
            self.time = params['time'] if 'time' in params else None
            self.exam_flg = params['exam_flg'] if 'exam_flg' in params else None
            self.groups = params['groups'].strip() if 'groups' in params else None
            self.discipline = params['discipline'] if 'discipline' in params else None
            self.tutors = params['tutors'] if 'tutors' in params else None
            self.comments = params['comments'] if 'comments' in params else None
            self.date = params['date'] if 'date' in params else None
            self.group_id = params['group_id'] if 'group_id' in params else None
            self.time_num = params['time_number'] if 'time_number' in params else None
            self.week_id = params['week_id'] if 'week_id' in params else None
            self.snap_id = params['snap_id'] if 'snap_id' in params else None
            self.time_start = params['time_start'] if 'time_start' in params else None
            self.time_end = params['time_end'] if 'time_end' in params else None
        else:
            raise TypeError('Пара: неверный входной параметр')

    def get_message(self):
        text_message = """{6} [{0} Пара: {1}]\n» {2},\n» {3},\n» {4} {5}\n╴╴╴╴╴╴╴╴╴╴╴\n""".format(
            self.time_num, self.time, self.discipline, self.groups if self.groups != '' else '(группы не указаны)',
            self.tutors if self.tutors != '' else '(нет информации)', self.comments, EMODJI.get('pin')).replace(', ]',']')
        return text_message


class User:
    """
    Класс для формирования объектов пользователей
    """

    def __init__(self, user=None, connection=Connection()):
        connection = Connection()
        user_row = Query("""select u.*, g.group_name, g.group_id from "user" u  
        left join "group" g on u.user_group_id = g.group_id
         where user_id = '{user_id}'
         """, connection).fetchall(
            user_id=user.id)

        self.connection = connection

        if len(user_row) == 0:
            Query("""insert into "user" (user_id, user_name) values ('{id}', '{name}') """, connection).execute(
                id=user.id, name=user.username)
            self.id = user.id
            self.name = user.username
            self.group_id = None
            self.group_name = None
            self.faculty = None
            self.add_group_id = None
        else:
            user = user_row[0]
            self.id = user['user_id']
            self.name = user['user_name']
            self.group_id = user['group_id']
            self.group_name = user['group_name']
            self.faculty = None
            self.add_group_id = user['additional_group_id']

        self.connection.connection.close()

    def get_group(self):
        return self.group_name

    def get_add_group(self):
        connection = Connection()
        row = Query("""select group_name from public."group" WHERE group_id = {id} """, connection).fetchone(
            id=self.add_group_id)
        return row[0]

    def get_group_id(self):
        return self.group_id

    def get_add_group_id(self):

        return self.add_group_id

    def set_group(self, group_id=None, group_name=None):
        connection = Connection()
        self.group_id = group_id
        self.group_name = group_name
        Query("""update "user" set user_group_id = {id}, user_group_name = '{name}' where user_id = '{user_id}' """,
              self.connection).execute(id=group_id, name=group_name, user_id = self.id, connection=connection)

    def set_add_group(self, group_id=None):
        connection = Connection()
        self.add_group_id = group_id
        Query("""update "user" set additional_group_id = {id} where user_id = '{user_id}' """,
              self.connection).execute(id=group_id, user_id=self.id, connection=connection)

    def show_faculty(self):
        connection = Connection()
        faculty = Query("""select faculty_desc, faculty_id from "faculty" where faculty_act_flg = 'Y' """, connection).fetchall()
        return faculty

    def get_groups_by_faculty(self, faculty):
        connection = Connection()
        if self.faculty is None:
            self.faculty = faculty
            #TODO: update таблицу юзера
        group_row = Query("""select group_name from "group" where group_faculty_id = '{faculty}' """, connection).fetchall(
            faculty=faculty)
        return group_row

    def find_group(self, group_name=None):
        conn = Connection()
        group_up = str(group_name).upper()
        group_row = Query(sql="""select group_id, group_name from "group" where upper(group_name) = '{group_name}' """,
                          connection=conn).fetchone(group_name=group_up)
        if group_row:
            return group_row
        else:
            return []

    def find_snap_date(self):
        conn = Connection()
        snap_dttm = Query("""select t2.snap_dttm
                              from "actual_snap" t1
                              inner join registry_snap t2 on (t1.snap_id = t2.snap_id and t1.group_id = t2.snap_group_id)
                              where t1.group_id = {group_id}
                               """, conn).fetchall(group_id=self.group_id)
        snap_dttm = snap_dttm[0]['snap_dttm'] if snap_dttm else None
        return snap_dttm




def get_users_list():
    conn = Connection()
    users = Query("""select user_id from "user"
                           """, conn).fetchall()
    users = [u.get('user_id') for u in users]
    return users

