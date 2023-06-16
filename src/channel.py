import json
import os

# необходимо установить через:
# pip install google-api-python-client
from googleapiclient.discovery import build


def printj(dict_to_print: dict) -> None:
    """Выводит словарь в json - подобном удобном формате с отступами"""
    print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))


class Channel:
    """Класс для ютуб - канала"""
    # YT_API_KEY скопирован из гугла и вставлен в переменные окружения
    api_key: str = os.getenv('YT_API_KEY')

    # создать специальный объект для работы с API
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала.
Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.channel = self.youtube.channels().list(id=self.channel_id, part='snippet, statistics').execute()
        self.title = self.channel['items'][0]['snippet']['title']
        self.description_title = self.channel['items'][0]['snippet']['description']
        self.url = self.channel['items'][0]['snippet']['thumbnails']['default']['url']
        self.subscriber_count = self.channel['items'][0]['statistics']['subscriberCount']
        self.video_count = self.channel['items'][0]['statistics']['videoCount']
        self.view_count = self.channel['items'][0]['statistics']['viewCount']

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=cls.api_key)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        printj(self.channel)

    @property
    def channel_id(self):
        return self.__channel_id

    def to_json(self):
        d = {}
        d['Channel'] = []
        d['Channel'].append({
            'channel_id': self.__channel_id,
            'title': self.title,
            'description_title': self.description_title,
            'url': self.url,
            'subscriber_count': self.subscriber_count,
            'video_count': self.video_count,
            'view_count': self.view_count
        })

        with open('moscowpython.json', 'w', encoding='utf-8') as file:
            json.dump(d, file, sort_keys=False, indent=4, separators=(',', ': '), ensure_ascii=False)

        with open('moscowpython.json',  encoding='utf-8') as f:
            print(json.load(f))



