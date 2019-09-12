import requests
from database import *
import datetime
import bs4 as BeautifulSoup
import re
import lxml
import config

def get_week_type(dttm=None):
    '''
    TODO: Реализовать определение типа недели
    :param dttm: 
    :return: 
    '''
    return 1


def schedule_load_by_group(group_id=None, snap_id=None, date_start=config.START_DT, date_end=config.END_DT):

    session = requests.Session()
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36 OPR/47.0.2631.71'}
    payload = {'Login': config.LOGIN, 'Pwd': config.PASS}
    r = session.post(url='https://portal.fa.ru/CoreAccount/LogOn', data=payload, headers=headers)


    schedule = {'AreaId': '0',
                'Date': date_start,
                'DateBegin': date_start,
                'DateEnd': date_end,
                'DepartmentId': '0',
                'FacultyId': '0',
                'GroupId': group_id,
                'JobType': 'GROUP',
                'TutorId': '0',
                'FacultyValue':'',
                'Tutor':'',
                'DepartmentValue':'',
                'AreaValue':''
                }
    r = session.post(url='https://portal.fa.ru/Job/SearchAjax', data=schedule, headers=headers)


    html = r.text

    records = []

    print(date_start)
    print(date_end)
    
    def my_parse(html):
        soup = BeautifulSoup.BeautifulSoup(html, "lxml")
        table2 = soup.find_all('table')[0]
        for tr in table2.find_all('tr')[0:]:
            tds = tr.find_all('td')
            records.append([elem.text for elem in tds])


    my_parse(html)
    jobs = []

    d1= datetime.datetime.strptime(records[1][0][0:10],'%d/%m/%Y')


    for i, rec in enumerate(records):
        if i != 0:
            try:
                d1 = datetime.datetime.strptime(rec[0][0:10], '%d/%m/%Y')
            except ValueError:
                rec.append(d1)
                jobs.append(rec)

    for i, recs in enumerate(jobs):
        jobs[i][0] = recs[0].replace('\n',', ')
        jobs[i][0] = recs[0].replace(', ', ' - ',2)
        jobs[i][0] = recs[0].replace(' - ', '',1)
        jobs[i][5] = re.sub("\s*\n\s*", ' ', recs[5].strip())
        jobs[i][4] = re.sub("\s*\n\s*", ' ', recs[4].strip())

    conn = Connection()
    time_list = Query(sql='select * from time_class', connection=conn).fetchall()

    class_list = []
    for i, row in enumerate(jobs):
        if (row[0] == '\xa0' or row[0] == '') and i != 0:
            if jobs[i-1][0] != '\xa0':
                row[0] = class_list[i-1]['time']
            else:
                row[0] = class_list[i-2]['time']

        time_id = 99
        for time in time_list:
            if row[0][:13] == time['time_str']:
                time_id = time['time_id']
                break
        week_id = get_week_type(dttm=row[6])

        time_str = row[0].lower()
        if time_str.find('зачет') != -1 or time_str.find('зачёт') != -1 or time_str.find('экзамен') != -1:
            exam_flg = 'Y'
        else:
            exam_flg = 'N'
        class_row = dict({
            'time': row[0], 'groups': row[1],
            'discipline': row[3], 'tutors': row[5],
            'comments': row[2] + ' ' + row[4],
            'date': row[6].date().isoformat(),
            'group_id': group_id,
            'time_id': time_id,
            'week_id': week_id,
            'snap_id': snap_id,
            'exam_flg': exam_flg
        })
        class_list.append(class_row)

    sql = '''
    INSERT INTO "schedule" (time, groups, discipline, tutors, comments, date, group_id, time_id, 
    week_id, snap_id, exam_flg) VALUES  
    '''
    print("len: {0}".format(len(class_list)))
    for class_row in class_list:
        sql += """('{time}', '{groups}', '{discipline}', '{tutors}', '{comments}', '{date}', {group_id}, {time_id}, {week_id}, {snap_id}, '{exam_flg}'),"""
        sql = Query(sql=sql, connection=conn).generate(**class_row)

    Query(sql=sql[:-1], connection=conn).execute(**class_row)

