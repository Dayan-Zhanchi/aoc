import os
from configparser import ConfigParser
from requests.exceptions import RequestException
import requests
import time


def download_input(day, file_name, input_dir):
    # save the file, so only need to download once to avoid unnecessary http requests
    if not os.path.isfile(file_name):
        config = ConfigParser()
        config.read('scraping.ini')
        base_url = config['MAIN']['BaseUrl']
        url = f"{base_url}/{day}/input"
        cookie_value = config['SESSION']['CookieSessionAOC']
        cookie = {'session': cookie_value}
        delay = config.getint('MAIN', 'Delay')
        retries = config.getint('MAIN', 'Retries')

        res = fetch_data(url, cookie, delay, retries)
        if not os.path.isdir(input_dir):
            os.makedirs(input_dir)
        if res:
            with open(file_name, 'wb') as f:
                f.write(res)


# TODO: There are some patterns, but they are not all consistent. Will have to look at this later. There are some parser that can extract sample inputs
#  already, but not with 100% accuracy if it isn't hardcoded after the fact: https://github.com/wimglenn/aocd-example-parser
def download_sample_input(day, file_name, input_dir):
    pass


def fetch_data(url, cookie, delay, retries=5):
    try:
        time.sleep(delay)
        response = requests.get(url, cookies=cookie)
        response.raise_for_status()
        return response.content
    except requests.exceptions.HTTPError as e:
        if 300 <= int(e.response.status_code) < 500:
            raise SystemExit(e)
        else:
            if retries > 0:
                print(f"Error: {e}. Retrying...")
                time.sleep(2 ** (- retries))
                return fetch_data(url, cookie, delay, retries - 1)
            else:
                print(f"Max retries reached.")
                raise SystemExit(e)
    except RequestException as e:
        raise SystemExit(e)
