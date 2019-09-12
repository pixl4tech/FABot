import requests
import config
import json
import database


session = requests.Session()
print(session.cookies.get_dict())
response = session.get('https://portal.fa.ru/CoreAccount/LogOn')
print(session.cookies.get_dict())

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36 OPR/47.0.2631.71'}
payload = {'Login': config.LOGIN, 'Pwd': config.PASS}
r = session.post(url='https://portal.fa.ru/CoreAccount/LogOn', data=payload, headers=headers)
print(session.cookies.get_dict())

groups_params = {'Name': ''}
r = session.post(url='https://portal.fa.ru/CoreGroup/SearchResultAjax', data=groups_params, headers=headers)

json_txt = r.text
groups_list = json.loads(json_txt)['data']

conn = database.Connection()
sql = 'INSERT INTO "group" (group_id, group_name, group_faculty_desc, group_create_dttm, group_stud_cnt, group_active) VALUES  '

for group in groups_list:
    sql += "({group_id}, '{group_name}', '{group_faculty_desc}', '{group_create_dttm}', {group_stud_cnt}, '{group_active}'),".format(
        group_id=group['id'], group_name=group['name'], group_faculty_desc=group['los'],
        group_create_dttm=group['datecreate'], group_stud_cnt=group['usersnum'],
        group_active= 'N' if group['name'][0] == '*' else 'Y'
    )

print(sql[:-1])
database.Query(sql=sql[:-1], connection=conn).execute()


