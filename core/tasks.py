import csv
from redis import Redis
from celery import shared_task
from pathlib import Path
from tempfile import NamedTemporaryFile
from urllib.parse import urljoin
from hillel import settings as project_settings
import requests
from django.db import connection


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent

DEBUG = True
ROOT_URLCONF = __name__

# os.environ.setdefault('DJANGO_SETTINGS_MODULE')

BASE_URL = 'https://data.gov.ua/dataset/4cced549-1a03-4e0b-afbb-461febb26007/resource/b4d8df31-8ecc-4646-a373-95b756fde8ea/download/'

CREATE = {
    'immunization_vaccine_codes': 'create table if not exists immunization_vaccine_codes (vaccine_code char(20), vaccine_name text)',
    'immunization_legal_entities_info': 'create table if not exists immunization_legal_entities_info (legal_entities_info char(20), vaccine_name text)',
    'immunization_covid19_2021': 'create table if not exists immunization_covid19_2021 (immunization_covid19_2021 char(20), vaccine_name text)',

}


DJANGO_SETTINGS_MODULE = project_settings

tmp = NamedTemporaryFile(delete=False)

@shared_task
def insert_into_db(tblname):
    create = CREATE[tblname]

    # создаем таблицу, если еще не создана

    with connection.cursor() as cur:
        cur.execute(create)
        print(f'create {tblname}', cur.rowcount)

    # удаляем старые записи
        delete = f'delete from {tblname}'
        cur.execute(delete)
        print(delete, cur.rowcount)

    # вставляем записи из файла

    with open(tmp.name) as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        names = ','.join(header)
        values = ','.join(['%s'] * len(header))
        insert = f'insert into {tblname} ({names}) values ({values})'
        with connection.cursor() as cur:
            cur.executemany(insert, reader)
            print(insert, cur.rowcount)


@shared_task
def load_file(fname):
    redis_client = Redis()
    old_e_tag = str(redis_client.get('old_e_tag'))
    headers = {'If-None-Match': old_e_tag[2:-1]}
    url = urljoin(BASE_URL, fname + '.csv')
    response = requests.get(url, stream=True, headers=headers)

    with response as res:
        if res.status_code == requests.codes.ok:  # 200
            redis_client.set('old_e_tag', res.headers.get('ETag'))
            # пишем данные в файл по мере поступления :)
            for chunk in res.iter_content(chunk_size=8192):
                tmp.write(chunk)
        else:
            print(f'{fname}: {res.reason} {res.status_code}')
    redis_client.close()

tmp.close()
#if __name__ == '__main__':
#   try:
#       tmp = NamedTemporaryFile(delete=False)
#       load_file.delay(('immunization_vaccine_codes', tmp))
#       tmp.close()
#       insert_into_db.delay((('immunization_vaccine_codes', tmp.name)))
#   except Exception:
#        print('TODO: delete {tblname}')
#       # os.unlink()
