import json
import os

# необходимо установить через:
# pip install google-api-python-client
from googleapiclient.discovery import build


class Video:
    """
    Класс для видео из ютуб - канала
    """
    # YT_API_KEY скопирован из гугла и вставлен в переменные окружения
    api_key: str = os.getenv('YT_API_KEY')

    # создать специальный объект для работы с API
    youtube = build('youtube', 'v3', developerKey=api_key)
    """
  - id видео - video_id
  - название видео - title
  - ссылка на видео - url
  - количество просмотров - view_count
  - количество лайков - like_count
    """
    def __init__(self, video_id):
        self.video_id = video_id
        self.video = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails', id=','.join([video_id])).execute()
        self.title = self.video['items'][0]['snippet']['title']
        self.url = 'https://www.youtube.com/watch?v='+ self.video_id
        self.view_count = self.video['items'][0]['statistics']['viewCount']
        self.like_count = self.video['items'][0]['statistics']['likeCount']

    def __str__(self):
        return f'{self.title}'


class PLVideo(Video):
    """
    Класс для видео `PLVideo`, который инициализируется  'id видео' и 'id плейлиста'
> Видео может находиться в множестве плейлистов, поэтому непосредственно из видео через API информацию о плейлисте не получить.
- Реализуйте инициализацию реальными данными следующих атрибутов экземпляра класса `PLVideo`:
  - id видео
  - название видео
  - ссылка на видео
  - количество просмотров
  - количество лайков
  - id плейлиста
    """

    def __init__(self, video_id, ply_id):
        super().__init__(video_id)
        self.ply_id = ply_id

