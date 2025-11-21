from typing import Optional
import requests
import math

class CatImageWithText:
    """Класс для получения случайных фотогрфий кошек c текстом"""

    BASE_URL = 'https://cataas.com'

    def __init__(self, text: str):
        if not text or text.strip() == "":
            raise ValueError("Текст не может быть пустым")

        cat_image = self._get_cat_with_text(text)
        if cat_image is not None:
            self.id = cat_image['id']
            self.url = cat_image['url']
        self.text = text
        image_info = self._get_image_info()
        if image_info:
            self.size = image_info['size']
            self.file_name = image_info['file_name']
        
    def _get_cat_with_text(self, text: str) -> Optional[dict]:
        """Метод получения фотографии с текстом"""
        if not text:
            return None
        try:
            response = requests.get(f'{self.BASE_URL}/cat/says/{text}', params = {'json': True})   
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            return None
        
    def _get_image_info(self):
        """Метод получения информации о картинке"""
        response = requests.get(f'{self.BASE_URL}/cat/{self.id}')   
        if response.status_code != 200:
            return False
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = int(math.floor(math.log(len(response.content), 1024)))
        p = math.pow(1024, i)
        s = round(len(response.content) / p, 2)

        mimetype = response.headers['Content-Type'].split('/')[1]
        file_name = f'{self.text}.{mimetype}'
        
        return {'size': (s, size_names[i]), 'file_name': file_name}


    def __str__(self):
        return self.url