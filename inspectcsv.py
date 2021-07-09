import sys
import csv
import uuid
from datetime import datetime

from django.core.exceptions import ValidationError
from django.core.validators import validate_email, URLValidator


# get_full_record возвращает первый запрос в котором все колонки заполнены,
# чтобы по содержимому колонок установить тип полей
def get_full_record(all_records):
    for record in range(1, len(all_records) - 1):
        count = 0
        for data in all_records[record]:
            if data != '':
                count += 1
        if len(all_records[0]) == count:
            return all_records[record]


# get_max_length находит наибольшее значение поля или проверяет равно ли это
# значение, для всех записей
def get_max_length(index, all_values):
    equal = 0
    current_record = get_full_record(all_values)
    for record in all_values:
        if len(record[index]) > len(current_record[index]):
            current_record = record

        if len(record[index]) == len(current_record[index]):
            equal += 1
    max_length = len(current_record[index])
    return max_length if equal == len(all_values) else max_length + int(
        (max_length / 4))


# integer_max проверяет колонки для целочисленных с целью установить
# подходящий тип поля
#     PositiveSmallIntegerField,
#     PositiveIntegerField,
#     PositiveBigIntegerField;
def integer_max(index, all_values):
    current_record = 0
    for record in all_values:
        if int(record[index]) > current_record:
            current_record = int(record[index])
    return current_record


# integer_min проверяет являться ли значение в полк для хранения
# целочисленніх значений отрицательнім и если да, то какой у них тип
# SmallIntegerField() или #IntegerField
def integer_min(index, all_values):
    current_record = 0
    for record in all_values:
        if int(record[index]) < current_record:
            current_record = int(record[index])
    return current_record


# get_type принимает поле записи возвращаемой get_full_record, индекс этой
# записи в запросе, а также все записи. Возвращает подходящее поле для
# каждой колонки
def get_type(field, index, all_values):
    try:
        int(field)
        int_field = integer_max(index, all_values)
        if integer_min(index, all_values) >= 0:
            if int_field <= 32767:
                type_field = '= models.PositiveSmallIntegerField()'
            elif int_field <= 2147483647:
                type_field = '= models.PositiveIntegerField()'
            else:
                type_field = '= models.PositiveBigIntegerField()'
        else:
            if int_field <=  32767and integer_min(index, all_values) >= -32768:
                type_field = '= models.SmallIntegerField()'
            else:
                type_field = '= models.IntegerField()'
        return type_field
    except ValueError:
        pass

    try:
        float(field)
        return '= models.FloatField()'
    except ValueError:
        pass

    try:
        uuid.UUID(field)
        return '= models.UUIDField(primary_key=True, default=uuid.uuid4)'
    except ValueError:
        pass

    try:
        validate_email(field)
        return '= models.EmailField(max_length={})'.format(
            get_max_length(index, all_values))
    except ValidationError:
        pass

    try:
        URLValidator()(field)
        return '= models.URLField(max_length={})'.format(
            get_max_length(index, all_values))
    except ValidationError:
        pass

    try:
        datetime.strptime(field, '%Y-%m-%d')
        return '= models.DateField()'
    except ValueError:
        pass

    if field in ('True', 'False', 'true', 'false'):
        return '= models.BooleanField()'

    return '= models.ChairField(max_length={})'.format(
        get_max_length(index, all_values))


def model_generator(csv_file=None):
    print()
    with open(csv_file, encoding='utf-8', newline='') as file:
        all_records = tuple(csv.reader(file))

    col_value = get_full_record(all_records)

    print('class {0}{1}'.format(csv_file[0:-4].capitalize(), '(models.Model)'))
    for index in range(len(all_records[0]) - 1):
        print()
        print('    {0} {1}'.format(all_records[0][index],
                                   get_type(col_value[index], index,
                                            all_records[1:])))


if __name__ == '__main__':
    print()
    if len(sys.argv) < 2 or not sys.argv[1].endswith('.csv'):
        raise TypeError('You must pass the name of the csv file as an argument')
    model_generator(sys.argv[1])

