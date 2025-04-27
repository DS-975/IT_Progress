from os.path import split

Text = '''
- График обучения
     - Кто, когда может присутствовать на обучение 
       (Бот будет за этим следить и 
        напоминать за 20 минут до урока в этот день
        Писать о прогулах и фиксить это в статистику)
        
   - Вывод статистики по обучению
     - ИМЯ
     - Был на обучение в такой-то день
     - Учился столько-то часов
     - Изучил вот это
     - Выходил в звонок 
   
   - Выводить информацию по встречам (Звонок)
     - Когда были встречи
     - Кто присутствовал на встрече 
   
   - Вывод информации, кто когда приступил к обучению
     (Например, 
               - ИМЯ готов учиться сейчас, 
               - Отошёл ИМЯ (отходить можно !> 10 минут),
                        если не отписался просто остальное время не идёт в отчёт
               - ИМЯ на сегодня закончил учёбу
               
   - Фиксить прогресс через БД 
     и выводить в определенное время статистику 
     по ученикам (Кто присутствует, 
                  какое направление, 
                  соответствие с графиком обучения,
                  были созвоны, 
                  включал демку)
'''

res_0 = []

res = Text.split('\n')

for _ in res:

    res_0.append(_ + '/n')

#print(res_0)

# Замена / на \
new_paths = [_.replace("/", "\\") for _ in res_0]

#print(new_paths)







import datetime

# Текущая дата и время
now = datetime.datetime.now()
print(f"Текущая дата и время: {now}")

# Форматирование текущей даты и времени
formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")
print(f"Отформатированная текущая дата и время: {formatted_now}")

# Создание объекта timedelta для добавления дней к текущей дате
delta_days = datetime.timedelta(days=7)
future_date = now + delta_days

# Вывод будущей даты через неделю
formatted_future_date = future_date.strftime("%Y-%m-%d %H:%M:%S")
print(f"Дата через неделю: {formatted_future_date}")

# Парсинг строки в объект datetime
date_string = "2023-10-15"
parsed_date = datetime.datetime.strptime(date_string, "%Y-%m-%d")
print(f"Парсинг строки '{date_string}' в объект date: {parsed_date.date()}")



import calendar
import datetime

# Получаем текущий год
year = datetime.datetime.now().year

# Список для хранения информации о месяцах
months_info = []

# Проходим по всем месяцам от 1 до 12
for month in range(1, 13):
    # Получаем количество дней в месяце
    days_in_month = calendar.monthrange(year, month)[1]

    # Получаем первый день недели для первого дня месяца (0 - понедельник, 6 - воскресенье)
    first_weekday = calendar.monthrange(year, month)[0]

    # Преобразуем номер дня недели в строку
    weekday_names = [1, 2, 3, 4, 5, 6, 7]
    first_weekday_name = weekday_names [first_weekday]

    # Добавляем информацию о месяце в список
    months_info.append((calendar.month_name[month], days_in_month, first_weekday_name))


#print(months_info)




# Текущей месяц
formatted_now = int(datetime.datetime.now().strftime("%m"))
print(f"Текущей месяц: {formatted_now}")

res_01 = []

for month_name, days, first_day in months_info:
    if month_name == calendar.month_name[int(datetime.datetime.now().strftime("%m"))]:
        print(month_name, days, first_day)

        res_01 = [ _ for _ in range(1, int(days)+1)]

        res_02 = []
        for _ in range(1, int(first_day)):
            res_02.append('.')
        print(res_02)

        res_01 = res_02 + res_01

        # if int(first_day) == 2:
        #     for day in range(1, int(days)+1):
        #         res_00.append(str(day))

#print(res_01)

# for day in range(1, calendar.month_name[int(datetime.datetime.now().strftime("%m")])

print(calendar.month_name[int(datetime.datetime.now().strftime("%m"))])











