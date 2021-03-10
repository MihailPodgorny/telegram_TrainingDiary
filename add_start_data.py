from db import create, get_id_by_name
from models import MuscleGroups, Exercises

# добавляем группы мышц
create(MuscleGroups(name='грудные',
                    text_href='http://sportwiki.to/%D0%9C%D1%8B%D1%88%D1%86%D1%8B_%D0%B3%D1%80%D1%83%D0%B4%D0%B8'))
create(MuscleGroups(name='спина',
                    text_href='http://sportwiki.to/%D0%9C%D1%8B%D1%88%D1%86%D1%8B_%D1%81%D0%BF%D0%B8%D0%BD%D1%8B'))
create(MuscleGroups(name='ноги',
                    text_href='http://sportwiki.to/%D0%9C%D1%8B%D1%88%D1%86%D1%8B_%D0%BD%D0%BE%D0%B3'))
create(MuscleGroups(name='плечи',
                    text_href='http://sportwiki.to/%D0%9C%D1%8B%D1%88%D1%86%D1%8B_%D0%BF%D0%BB%D0%B5%D1%87%D0%B5%D0%B2%D0%BE%D0%B3%D0%BE_%D0%BF%D0%BE%D1%8F%D1%81%D0%B0'))
create(MuscleGroups(name='руки',
                    text_href='http://sportwiki.to/%D0%9C%D1%8B%D1%88%D1%86%D1%8B_%D1%80%D1%83%D0%BA'))
create(MuscleGroups(name='прочее',
                    text_href='http://sportwiki.to/%D0%AD%D0%BD%D1%86%D0%B8%D0%BA%D0%BB%D0%BE%D0%BF%D0%B5%D0%B4%D0%B8%D1%8F_%D0%B1%D0%BE%D0%B4%D0%B8%D0%B1%D0%B8%D0%BB%D0%B4%D0%B8%D0%BD%D0%B3%D0%B0'))

# добавляем упражнения
create(Exercises(name='жим_лежа',
                 group_id=get_id_by_name(MuscleGroups, 'грудные'),
                 original_name='Bench press'))
create(Exercises(name='становая_тяга',
                 group_id=get_id_by_name(MuscleGroups, 'прочее'),
                 original_name='Deadlifts'))
create(Exercises(name='приседания',
                 group_id=get_id_by_name(MuscleGroups, 'ноги'),
                 original_name=''))
create(Exercises(name='жим_гантелей_30',
                 group_id=get_id_by_name(MuscleGroups, 'грудные'),
                 original_name='Bench press 30'))

