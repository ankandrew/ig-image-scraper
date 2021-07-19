from ihs import Scraper, Downloader

if __name__ == "__main__":
    credentials = {
        'username': 'your_username',
        'password': 'your_password'
    }
    urls_path = 'scraped/urls.txt'
    Scraper(login=credentials,
            max_samples=10,
            url_save_path=urls_path,
            driver_path='driver/chromedriver.exe').scan(tag='happy')
    Downloader(url_file=urls_path,
               img_folder='img/').start(wait_time=1.0)
