# -*- coding: utf-8 -*-

import requests
import re
from database import *
import datetime


def track(inline=False, action=None, message=None):
    action_txt = re.sub(r"""['"\s;]""", "_", message.text[:99])

    data = {'user_id': message.chat.id,
            'user_name': message.chat.username,
            'user_first': message.chat.first_name,
            'user_last': message.chat.last_name,
            'action_type': action,
            'action_txt': action_txt,
            'mode_type': 'I' if inline else 'T',
            'request_dt': datetime.datetime.today().date().isoformat()
            }

    conn = Connection()
    Query("""
        INSERT INTO public.request_log 
        (user_id, user_name, user_first, user_last, action_type, action_txt, mode_type, request_dt) 
        VALUES ('{user_id}', '{user_name}', '{user_first}', '{user_last}', '{action_type}', '{action_txt}', 
        '{mode_type}', '{request_dt}');
                           """, conn).execute(**data)



def users_count():
    conn = Connection()
    row = Query(""" select * from public.count_users
                           """, conn).fetchone()
    return row[0]

def new_users_per_day(dttm):
    conn = Connection()
    row = Query("""select count(*) from  public."user" where user_create_dttm >= '{dt}' """, conn).fetchone(
        dt=dttm.date().isoformat())
    return row[0]

def users_per_day(dttm):
    conn = Connection()
    row = Query("""
        select count(a.*) from (
            select DISTINCT user_id from  public."request_log" where request_dt = '{dt}') a """, conn).fetchone(
        dt=dttm.date().isoformat())
    return row[0]

def requets_per_day(dttm):
    conn = Connection()
    row = Query("""select count(*) from  public."request_log" where request_dt = '{dt}' """, conn).fetchone(
        dt=dttm.date().isoformat())
    return row[0]

def requets_print():
    conn = Connection()
    row_list = Query("""select * from  public."user_requests" limit 30 """, conn).fetchall()
    return row_list

def fac_users():
    conn = Connection()
    row_list = Query(""" select count(t.faculty_desc) as count, t.faculty_desc from (
  select u.user_id, f.faculty_desc
    from  public."user" u
    inner join public."group" g on u.user_group_id = g.group_id
    inner join public."faculty" f on g.group_faculty_id = f.faculty_id
     ) t
group by t.faculty_desc
ORDER BY count DESC 
    """, conn).fetchall()
    return row_list