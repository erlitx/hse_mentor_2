import csv
import requests

url = "https://storage.yandexcloud.net/hses3/logs_v2.txt"

response = requests.get(url)
response.raise_for_status()  # Проверка на ошибки

lines = response.text.splitlines()
reader = csv.DictReader(lines, delimiter='\t')

for row in reader:
    print(row)
