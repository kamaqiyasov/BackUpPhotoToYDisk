import configparser
import unittest
import requests

from src.YDConnection import YDConnection


class TestYandexDiskAPI(unittest.TestCase):
    
    def setUp(self):
        config = configparser.ConfigParser()
        config.read('config/settings.ini')
        self.token = config['Ydisk']['token']
        self.yd = YDConnection(self.token)
        self.test_folder = "test_folder_123"
        self.created_folders = []
        
    def tearDown(self):
        for folder in self.created_folders:
            requests.delete(
                f'{YDConnection.BASE_URL}/v1/disk/resources',
                params={'path': folder, 'permanently': True},
                headers={'Authorization': f'OAuth {self.token}'}
            )

    def test_upload_from_web_valid_url(self):
        folder = "test_upload_folder"
        self.created_folders.append(folder)
        
        self.yd.create_folder(folder)
        file_name = f"{folder}/test_image.png"
        valid_url = f"https://cataas.com/cat/mACGUDVn2tlR1z2B/says/dwad?position=center&font=Impact&fontSize=50&fontColor=%23fff&fontBackground=none"
        
        self.yd.create_folder(folder)
        
        result = self.yd.upload_from_web(valid_url, file_name)
        
        self.assertTrue(result)

    def test_create_folder_success(self):
        self.created_folders.append(self.test_folder)
        result = self.yd.create_folder(self.test_folder)
        self.assertTrue(result, "Папка не создана")

        folder_exists = self.yd.check_folder_exists(self.test_folder)
        self.assertTrue(folder_exists, "Папки нет на диске")

    def test_create_folder_already_exists(self):
        folder = "test_existing_folder"
        self.created_folders.append(folder)
        
        first_create = self.yd.create_folder(folder)
        self.assertTrue(first_create, "Первая папка не создана")
        
        second_folder = self.yd.create_folder(folder)
        self.assertTrue(second_folder)

    def test_create_folder_empty_path(self):
        result = self.yd.create_folder("")
        self.assertFalse(result, "Пустой путь должен возвращать False")

    def test_connection_with_invalid_token(self):
        invalid_yd = YDConnection("INVALID_TOKEN")
        result = invalid_yd.create_folder(self.test_folder)
        self.assertFalse(result, "Неверный токен должен возвращать False")