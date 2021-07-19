## Instagram Image Scraper

Scrap instagram images given a hashtag

### Usage

```python
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
```

### Installation

Run:

`pip install -r requirements.txt`

Then download the chrome driver from [here](https://chromedriver.chromium.org/downloads) according to your Chrome version.
When creating `Scraper` object make sure to pass the correct path to the driver.

### Disclaimer

This tool is for educational purposes only.