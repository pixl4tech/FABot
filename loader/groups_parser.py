import datetime
import bs4 as BeautifulSoup
import re
import os

directory = r'C:\Users'
files = os.listdir(directory)
grp_list = []

for file in files:
    f = open(r'{0}\{1}'.format(directory, file))
    html = f.read()
    f.close()
    soup = BeautifulSoup.BeautifulSoup(html, "lxml")
    form_data = soup.findAll(attrs={'class': re.compile(r"form-group")})

    group_id = file.split('.')[0]
    group_name = form_data[0].contents[3].text.strip()
    external_name = form_data[1].contents[3].text.strip()
    fac_name = form_data[2].contents[3].contents[1].contents[1].attrs['value'].strip()
    stud_count = form_data[5].contents[3].text.strip()
    create_dt = form_data[6].contents[3].contents[1].attrs['value'].strip()
    try:
        is_archive = bool(form_data[8].contents[1].contents[1].attrs.get('checked', False))
    except:
        is_archive = True
    is_true_name = bool(group_name == external_name)
    grp_list.append({
        "group_id": group_id,
        "group_name": group_name,
        "external_name": external_name,
        "is_true_name": is_true_name,
        "fac_name": fac_name,
        "stud_count": stud_count,
        "create_dt": create_dt,
        "is_archive": is_archive
    })

grp_actual = [grp for grp in grp_list if not grp['is_archive']]
grp_not_valid = [grp for grp in grp_list if not grp['is_true_name']]
print('enjoy')