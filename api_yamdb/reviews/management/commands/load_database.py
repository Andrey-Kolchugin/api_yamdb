import csv
import os
import sys
from django.conf import settings

from django.core.management import BaseCommand
from api_yamdb.settings import BASE_DIR

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class Command(BaseCommand):
    help = 'Заполняет базу данных из CSV файлов'
    print('Загрузка данных в базу...')

    def handle(self, *args, **options):
        models_data_dict = {}
        csv_list = list(filter(lambda x: x.endswith('.csv'),
                               os.listdir(BASE_DIR + '/static/data')
                               ))
        for table in csv_list:
            models_data_dict[table] = table[:-4].title()

        try:
            for csv_f, model in models_data_dict.items():
                with open(
                        f'{BASE_DIR}/static/data/{csv_f}',
                        'r',
                        encoding='utf-8'
                ) as csv_file:
                    reader = csv.DictReader(csv_file)
                    globals()[model].objects.bulk_create(
                        globals()[model](**data) for data in reader)

        except Exception as error:
            print(f'Сбой в работе программы: {error} ')
        finally:
            print('Работа команды завершена')

