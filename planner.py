
import loader.shedule_loader as loader
from database import *
import time

conn = Connection()
snap_id = Query("SELECT nextval('snap_id_seq'::regclass) as nextval", conn).fetchone()[0]

group_list = Query(""" SELECT group_id from "group" where group_active = 'Y' and group_load_flg = 'Y' """, conn).fetchall()

for g in group_list:
    print('*** Расписание для {0} начало загрузки ***'.format(g['group_id']))
    try:
        loader.schedule_load_by_group(group_id=g['group_id'], snap_id=snap_id,
                                      date_start=config.START_DT, date_end=config.END_DT)
        Query("""insert into "registry_snap" (snap_id, snap_group_id) VALUES ({snap_id}, {group_id})""", conn).execute(
            snap_id=snap_id, group_id=g['group_id'])
        Query("""
        INSERT INTO actual_snap (snap_id, group_id) 
        VALUES ({snap_id}, {group_id}) ON CONFLICT (group_id) DO UPDATE 
          SET  snap_id = {snap_id};
        """, conn).execute(
            snap_id=snap_id, group_id=g['group_id'])

        print('*** Расписание для {0} конец загрузки ***'.format(g['group_id']))
    except Exception as e:
        print('*** Расписание для {0} Ошибка {1} ***'.format(g['group_id'], e))
        time.sleep(1)
