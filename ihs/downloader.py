import urllib.request
from pathlib import Path
from time import sleep
from urllib.error import HTTPError

from tqdm import tqdm


class Downloader:
    def __init__(self, url_file: str, img_folder: str = 'img/'):
        url_file = Path(url_file)
        if not url_file.is_file():
            raise FileNotFoundError(f'{url_file} does not exist!')
        with open(url_file, 'r') as f:
            self.urls = f.readlines()
        self.img_folder_path = Path(img_folder)
        if not self.img_folder_path.exists():
            print(f'Path does not exist! Creating one ...')
            self.img_folder_path.mkdir(parents=True)

    def start(self, wait_time: float = 1.0):
        success, errors = 0, 0
        for url in tqdm(self.urls, desc='Img Downloader'):
            out_path = self.img_folder_path / url.split('/')[-1].split('?')[0]
            try:
                urllib.request.urlretrieve(str(url), out_path)
                sleep(wait_time)
                success += 1
            except HTTPError as e:
                errors += 1
        print(f'Failed: {errors / (errors + success)}')
        print(f'Success: {success / (errors + success)}')

