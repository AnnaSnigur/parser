from user_agent import generate_user_agent
from base import save_db
from utils import save_info, random_sleep, json_save
import requests
from bs4 import BeautifulSoup

# global variables
HOST = 'https://www.work.ua'
ROOT_PATH = '/ru/jobs/'


def main():
    page = 0

    while True:
        page += 1

        payload = {
            'ss': 1,
            'page': page,
        }
        user_agent = generate_user_agent()
        headers = {
            'User-Agent': user_agent,
        }

        print(f'PAGE: {page}')
        response = requests.get(HOST + ROOT_PATH, params=payload, headers=headers)
        random_sleep()
        response.raise_for_status()

        html = response.text

        soup = BeautifulSoup(html, 'html.parser')

        class_ = 'card card-hover card-visited wordwrap job-link'
        cards = soup.find_all('div', class_=class_)
        if not cards:
            cards = soup.find_all('div', class_=class_ + ' js-hot-block')

        result = []

        if not cards:
            break

        for card in cards:
            tag_a = card.find('h2').find('a')
            title = tag_a.text
            href = tag_a['href']
            path = requests.get(HOST + href, headers=headers)
            text = path.text
            soup = BeautifulSoup(text, 'html.parser')
            company = soup.find(class_='').find('b').text

            try:
                salary = soup.find(class_='').find('b').text
            except AttributeError:
                salary = 'No information'

            try:
                description = soup.find(id='job-description').find_all(['p', 'b', 'li'])
            except AttributeError:
                description = 'No information'

            result.append(
                [
                    f'Ссылка: {href},\n'
                    f'Вакансия: {title},\n'
                    f'Компания: {company},\n'
                    f'Зарплата: {salary},\n'
                    f'Описание: {description}\n'
                ]
            )
            save_db(href, title, salary, company, description)

            json_db = ({
                {
                    'Ссылка': href,
                    'Вакансия': title,
                    'Компания': company,
                    'Зарплата': salary,
                    'Описание': description.replace('\n', ''),
                }
            })
            json_save(json_db)
        save_info(result)


if __name__ == "__main__":
    main()
