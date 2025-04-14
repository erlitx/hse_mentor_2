
```bash
# Загрузка transactions_v2.csv 
curl -s https://storage.yandexcloud.net/hses3/transactions_v2.csv | \
clickhouse-client --query "INSERT INTO transactions_v2 FORMAT CSVWithNames"

# Загрузка logs_v2.txt
curl -s https://storage.yandexcloud.net/hses3/logs_v2.txt | \
clickhouse-client --query "INSERT INTO logs_v2 FORMAT TabSeparatedWithNames"


