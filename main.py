"""
Главный исполняемый файл
"""

import configparser
from src.YDConnection import YDConnection
from src.Cats import CatImageWithText
import json
import os

def main():
    config = configparser.ConfigParser()
    config.read('config/settings.ini')

    token = config['Ydisk']['token']
    group_name = config['NetologyGroup']['group_name']

    text_image = input('Введите текст для картинки: ')
    cat_image = CatImageWithText(text_image)
    disk = YDConnection(token)
    if disk.create_folder(group_name):
        if disk.upload_from_web(cat_image.url, f'/{group_name}/{cat_image.file_name}'):
            if not os.path.exists('log.json'):
                with open('log.json', 'w', encoding='utf-8') as file:
                    json.dump([], file)
            
            with open('log.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
            data.append({'url': cat_image.url, 'file': cat_image.file_name, 'size': f'{cat_image.size[0]} {cat_image.size[1]}'})

            with open('log.json', 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4)
        else:
            print("Ошибка при загрузке")
            
if __name__ == "__main__":
    main()
