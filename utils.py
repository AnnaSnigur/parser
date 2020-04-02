import random
from time import sleep
import json


def save_info(array: list) -> None:
    with open('workua.txt', 'a') as file:
        for line in array:
            file.write(' | '.join(line) + '\n')


def json_save(data: dict) -> None:
    with open('workua.json', 'a', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        f.write('\n')


def random_sleep():
    sleep(random.randint(1, 4))
