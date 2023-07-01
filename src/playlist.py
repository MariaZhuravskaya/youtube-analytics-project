import os

import isodate
from googleapiclient.discovery import build

from src.video import Video


class PlayList:
    """
    Класс для ютуб - канала
    """
    # YT_API_KEY скопирован из гугла и вставлен в переменные окружения
    api_key: str = os.getenv('YT_API_KEY')

    # создать специальный объект для работы с API
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id):

        self.playlist_id = playlist_id

        # Получение данных по play-листам канала
        self.playlist = self.youtube.playlists().list(id=playlist_id, part='contentDetails,snippet', maxResults=50).execute()

        # Получение id плейлиста
        self.playlist_videos = self.youtube.playlistItems().list(playlistId=playlist_id, part='contentDetails', maxResults=50).execute()

        # Получить все id видеороликов из плейлиста
        video_ids = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]

        # Вывести длительности видеороликов из плейлиста
        self.video_response = self.youtube.videos().list(part='contentDetails,statistics', id=','.join(video_ids)).execute()

        self.title = self.playlist['items'][0]['snippet']['title']
        self.url = 'https://www.youtube.com/playlist?list=' + playlist_id

    @property
    def total_duration(self):
        """
          Возвращает объект класса `datetime.timedelta` с суммарной длительность плейлиста
          """
        duration = isodate.duration.Duration()
        for video in self.video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = duration + isodate.parse_duration(iso_8601_duration)
        return duration.tdelta

    def show_best_video(self):
        """
        Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)
        """
        d = {}
        for like in self.video_response['items']:
            like_count = like['statistics']['likeCount']
            if d == {}:
                d.setdefault(like_count, 'https://youtu.be/' + like['id'])
            else:
                for key in d:
                    if like_count > key:
                        d.clear()
                        key = like_count
                        d[key] = 'https://youtu.be/' + like['id']
        for key in d:
            return d[key]
