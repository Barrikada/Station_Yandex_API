import requests

# Определяем API ключ и базовый URL для "Яндекс Расписаний"
API_KEY = '018d0068-399c-42b2-b5df-02d9afe0930e'
BASE_URL = 'https://api.rasp.yandex.net/v3.0/'


# Функция для поиска ближайших станций
def find_nearest_stations():
    url = f'{BASE_URL}nearest_stations/'
    params = {
        'apikey': API_KEY,
        'format': 'json',
        'lat': 53.195873,  # Широта Пензы
        'lng': 45.018316,  # Долгота Пензы
        'distance': 50,  # Радиус поиска в километрах
        'transport_types': 'train',  # Тип транспорта — поезд
        'limit': 10  # Максимальное количество результатов
    }
    response = requests.get(url, params=params)
    response.raise_for_status()  # Проверяем успешность запроса
    data = response.json()  # Преобразуем ответ в JSON
    return data


# Функция для получения расписания станции по её коду
def get_schedule(station_code):
    url = f'{BASE_URL}schedule/'
    params = {
        'apikey': API_KEY,
        'format': 'json',
        'station': station_code,  # Код станции
        'transport_types': 'train',  # Тип транспорта — поезд
        'event': 'departure',  # Тип события — отправление
    }
    response = requests.get(url, params=params)
    response.raise_for_status()  # Проверяем успешность запроса
    data = response.json()  # Преобразуем ответ в JSON
    return data


# Основная функция для тестирования ближайших станций и их расписания
def test_nearest_station_and_schedule():
    nearest_stations = find_nearest_stations()

    # Проверяем, что ответ содержит ключ 'stations'
    assert 'stations' in nearest_stations, "Ответ должен содержать ключ 'stations'"
    stations = nearest_stations['stations']

    # Проверяем, что в радиусе 50 км найдено как минимум 3 станции
    assert len(stations) >= 3, "Должно быть как минимум 3 станции в радиусе 50 км"
    third_station = stations[2]  # Третья ближайшая станция

    print(f"Третья ближайшая станция: {third_station['title']} (код: {third_station['code']})")

    # Получаем расписание по коду третьей станции
    schedule = get_schedule(third_station['code'])

    # Если расписание пустое, логируем это и пропускаем дальнейшие проверки
    if not schedule.get('schedule'):
        print(f"Для станции {third_station['title']} нет доступных рейсов.")
        return

    # Проверяем наличие обязательных ключей в ответе расписания
    required_keys = ['date', 'pagination', 'station', 'schedule']
    for key in required_keys:
        assert key in schedule, f"Ответ расписания должен содержать ключ '{key}'"

    # Проверяем наличие 'schedule_direction' и 'directions', если они присутствуют
    if 'schedule_direction' in schedule:
        assert schedule['schedule_direction'], "Направление расписания не должно быть пустым"
    if 'directions' in schedule:
        assert schedule['directions'], "Направления не должны быть пустыми"

    # Проверяем, что в каждом объекте 'thread' в массиве 'schedule' есть непустые элементы 'number', 'title', 'uid'
    for entry in schedule['schedule']:
        thread = entry.get('thread', {})
        assert 'number' in thread and thread['number'], "Объект 'thread' должен содержать непустой 'number'"
        assert 'title' in thread and thread['title'], "Объект 'thread' должен содержать непустой 'title'"
        assert 'uid' in thread and thread['uid'], "Объект 'thread' должен содержать непустой 'uid'"

    # Выводим результат (расписание)
    print(schedule)
    print("Все тесты пройдены успешно.")  # Если все тесты прошли успешно


# Запускаем основную функцию при выполнении скрипта
if __name__ == '__main__':
    test_nearest_station_and_schedule()
