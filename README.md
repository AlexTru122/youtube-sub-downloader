# YouTube Metadata and Transcript Scraper

Этот Python-скрипт позволяет получать метаданные и субтитры (если доступны) для всех видео на указанном YouTube-канале. Он собирает информацию о видео, такую как заголовок, описание, количество просмотров, лайков и многое другое, а затем сохраняет эти данные вместе с транскриптом видео в текстовые файлы.

## Возможности

- Получение метаданных для всех видео на указанном YouTube-канале.
- Сохранение деталей видео, таких как заголовок, описание, просмотры, лайки и другие параметры.
- Извлечение и сохранение субтитров (если доступны) на нескольких языках.
- Хранение всех данных в отдельных текстовых файлах, организованных по ID видео.

## Требования

Для использования этого скрипта вам необходимо:

- Python 3.x
- Google API Client: `google-api-python-client`
- YouTube Transcript API: `youtube-transcript-api`

Установите необходимые библиотеки с помощью pip:

```bash
pip install google-api-python-client youtube-transcript-api
```

## Установка
Клонируйте репозиторий:
```bash
git clone https://github.com/ваш-юзернейм/YouTube-Metadata-Scraper.git
cd YouTube-Metadata-Scraper
```
## Создайте и активируйте виртуальное окружение (рекомендуется):
```Для Linux/Mac:
python3 -m venv venv
source venv/bin/activate
```

## Конфигурация
Получите API-ключ YouTube Data API:

1. Перейдите в Google Cloud Console.
2. Создайте новый проект или выберите существующий.
3. Перейдите в APIs & Services > Library.
4. Найдите YouTube Data API v3 и включите его.
5. Перейдите в APIs & Services > Credentials.
6. Создайте API-ключ и скопируйте его.
7. Вставьте API-ключ в скрипт:

Откройте script.py (или как вы назвали файл) и вставьте ваш API-ключ:
```
API_KEY = ВАШ_API_КЛЮЧ
```


## Использование
Укажите хэндл канала:

В скрипте найдите строку:

```python
handle = "@cryptoillia"
Замените @cryptoillia на хэндл нужного вам YouTube-канала.
```
Запустите скрипт:

```python script.py```
Скрипт создаст папку subtitles и сохранит в ней текстовые файлы с метаданными и транскриптами видео.
