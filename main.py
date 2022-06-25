import requests
from bs4 import BeautifulSoup

#Посилання на сайт, який потрібно спарсити
url = 'https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D0%B3%D0%BE%D1%81%D1%83%D0%B4%D0%B0%D1%80%D1%81%D1%82%D0%B2'

#Отримуємо код та перевіряємо чи можемо спарсити сайт
r = requests.get(url)

#Перерводимо набір тегів в більш-менш читабельний текст
soup = BeautifulSoup(r.text, 'lxml')

#Парсимо таблицю, зробивши список з описів всіх країн
table = soup.find('div', class_='mw-body-content mw-content-ltr').find('table', class_='wikitable').find('tbody').findAll('tr')

#Ключі до майбутнього словника
keys = ['country', 'full_country_name', 'same_letter_count', 'flag_url']

#Робимо списки окремо по кожній країні (ця інформація в подальшому буде використана для створення словників по країнах)
list_information = []
for block in table:
    some_list = []
    content = block.findAll('td')
    for item in content:
        if item:
            some_list.append(item)
    if some_list:
        some_list[1] = block.find('span', class_='flagicon').find('a', class_='image').find('img', class_='thumbborder').get('src')
        some_list[2] = some_list[2].text[0:some_list[2].text.find('\\n')]
        some_list[3] = some_list[3].text[0:some_list[3].text.find('\\n')]
        list_information.append(some_list[1:])

#Визначаємо кількість країн, які начинаються з тієї ж самої букви, що і дана країна
for index, element in enumerate(list_information):
    first_letter_of_country = element[1][0]
    count_letter = 0
    for item in list_information:
        if item[1][0] == first_letter_of_country:
            count_letter += 1
    list_information[index].append(count_letter)

#Визначаємо кількість слів у повній назві країни
count_words_in_full_country_name = {}
for item in list_information:
    upd = {item[1]:len(item[2].split(' ')) }
    count_words_in_full_country_name.update(upd)

#Формуємо словник із інформації в списках та робимо список словників
for index in range(len(list_information)):
    list_information[index] = {
        keys[0] : list_information[index][1],
        keys[1] : list_information[index][2],
        keys[2] : list_information[index][3],
        keys[3] : list_information[index][0]
    }

#Функція яка виводить словник з даними конкретної країни по її короткому імені
def get_country(country_name):
    for item in list_information:
        if item.get('country') == country_name:
            return item

print('Вас вітає вільна енциклопедія - Вікіпедія')
print('Вам наданий матеріал про країни-члени ООН')
print('Якщо ви хочете вийти з програми, то введіть команду exit')

while True:
    print()
    country = input('Введіть назву країни російською мовою, або команду щоб вийти з програми: ')
    if country == 'exit':
        print()
        break
    result = get_country(country)
    if result:
        for key, value in result.items():
            print(key, ":", value)
    else:
        print('Такої країни не знайдено, введіть правильну назву.')

print('Ви використовували матеріал із вільної енциклопедії - Вікіпедії')