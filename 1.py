import os
from googleapiclient.discovery import build
from youtube_transcript_api import (
    YouTubeTranscriptApi,
    TranscriptsDisabled,
    NoTranscriptFound
)

API_KEY = ''


def get_channel_id_from_handle(youtube, handle: str) -> str:
    """
    handle = что-то вроде "@cryptoillia"
    Возвращает channelId в формате "UC..."
    """
    response = youtube.search().list(
        part="snippet",
        q=handle,
        type="channel",
        maxResults=1
    ).execute()

    items = response.get("items", [])
    if not items:
        return None

    return items[0]["id"]["channelId"]

def get_all_videos_from_channel(youtube, channel_id):
    """
    Возвращает список video_id (строк) всех видео на канале channel_id
    """
    videos = []
    page_token = None

    while True:
        response = youtube.search().list(
            part="id",
            channelId=channel_id,
            type="video",
            maxResults=50,
            pageToken=page_token
        ).execute()

        for item in response.get("items", []):
            videos.append(item["id"]["videoId"])

        page_token = response.get("nextPageToken")
        if not page_token:
            break

    return videos

def main():
    # 0) Инициализируем клиент YouTube Data API
    youtube = build("youtube", "v3", developerKey=API_KEY)

    # Создадим папку для хранения субтитров/метаданных (если её ещё нет)
    os.makedirs("subtitles", exist_ok=True)

    # 1) Получаем channel_id по handle (название канала)
    handle = "@cryptoillia"
    channel_id = get_channel_id_from_handle(youtube, handle)
    if not channel_id:
        print(f"Не удалось найти channelId для handle '{handle}'")
        return

    print("Найден channel_id =", channel_id)

    # 2) Собираем все video_id с канала
    video_ids = get_all_videos_from_channel(youtube, channel_id)
    print(f"Найдено видео: {len(video_ids)} шт.")

    # 3) Перебираем все видео
    for vid in video_ids:
        print(f"Обработка видео {vid} ...")

        # -- (A) Сначала получим метаданные о видео (название, превью, статистику и т.д.)
        try:
            meta_resp = youtube.videos().list(
                part="snippet,contentDetails,statistics",  # можно добавить/убрать нужные части
                id=vid
            ).execute()

            if not meta_resp["items"]:
                print(f"  Нет метаданных для видео {vid}")
                continue

            item = meta_resp["items"][0]
            snippet = item.get("snippet", {})
            statistics = item.get("statistics", {})
            content_details = item.get("contentDetails", {})

            title = snippet.get("title", "")
            description = snippet.get("description", "")
            published_at = snippet.get("publishedAt", "")
            channel_title = snippet.get("channelTitle", "")
            thumbnails = snippet.get("thumbnails", {})

            # Можем вытащить хотя бы одно превью (default / medium / high / ...)
            thumbnail_url = thumbnails.get("high", {}).get("url") \
                            or thumbnails.get("medium", {}).get("url") \
                            or thumbnails.get("default", {}).get("url") \
                            or "Нет превью"

            view_count = statistics.get("viewCount", "N/A")
            like_count = statistics.get("likeCount", "N/A")
            comment_count = statistics.get("commentCount", "N/A")

            duration = content_details.get("duration", "")  # например, "PT16M25S"
            dimension = content_details.get("dimension", "")  # "2d" или "3d"
            definition = content_details.get("definition", "")  # "hd" или "sd"

        except Exception as e:
            print(f"  Ошибка при получении метаданных для видео {vid}: {e}")
            continue

        # -- (B) Пытаемся получить субтитры
        transcript_data = None
        try:
            transcript_data = YouTubeTranscriptApi.get_transcript(vid, languages=["ru", "en"])
        except TranscriptsDisabled:
            print(f"  Субтитры для видео {vid} отключены (TranscriptsDisabled).")
        except NoTranscriptFound:
            print(f"  Нет доступных субтитров для видео {vid} (NoTranscriptFound).")
        except Exception as e:
            print(f"  Ошибка при получении субтитров для видео {vid}: {e}")

        # -- (C) Сохраняем всё в файл subtitles/<videoId>.txt
        file_path = os.path.join("subtitles", f"{vid}.txt")
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                # Заголовок: основные метаданные
                f.write(f"Video ID: {vid}\n")
                f.write(f"Title: {title}\n")
                f.write(f"Channel: {channel_title}\n")
                f.write(f"Published at: {published_at}\n")
                f.write(f"Views: {view_count}, Likes: {like_count}, Comments: {comment_count}\n")
                f.write(f"Thumbnail URL: {thumbnail_url}\n")
                f.write(f"Duration: {duration}, dimension={dimension}, definition={definition}\n")
                f.write("Description:\n")
                f.write(description.strip() + "\n\n")

                # Субтитры (если удалось получить)
                if transcript_data:
                    f.write("=== TRANSCRIPT ===\n")
                    for line in transcript_data:
                        start = line["start"]
                        duration_line = line["duration"]
                        text = line["text"]
                        f.write(f"[start={start:.2f}, dur={duration_line:.2f}] {text}\n")
                else:
                    f.write("=== NO TRANSCRIPT AVAILABLE ===\n")

            print(f"  Файл сохранён: {file_path}")
        except Exception as e:
            print(f"  Ошибка при записи файла {file_path}: {e}")

if __name__ == "__main__":
    main()
