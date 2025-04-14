from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

with DAG(
    dag_id='replicate_hive_to_clickhouse',
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval='@daily',
    catchup=False,
    tags=['replication', 'clickhouse', 'hive'],
) as dag:

    # 1. Экспорт transactions_v2 из Hive 
    export_transactions = BashOperator(
        task_id='export_transactions',
        bash_command="""
        hive -e "SELECT * FROM transactions_v2" \
        | sed 's/[\t]/,/g' > /tmp/transactions_v2.csv
        """,
    )

    # 2. Загрузка в ClickHouse
    load_transactions = BashOperator(
        task_id='load_transactions',
        bash_command="""
        clickhouse-client --query="TRUNCATE TABLE transactions_v2";
        clickhouse-client --query="INSERT INTO transactions_v2 FORMAT CSVWithNames" < /tmp/transactions_v2.csv
        """,
    )

    # 3. Экспорт logs_v2 из Hive 
    export_logs = BashOperator(
        task_id='export_logs',
        bash_command="""
        hive -e "SELECT * FROM logs_v2" > /tmp/logs_v2.csv
        """,
    )

    # 4. Загрузка logs_v2 в ClickHouse
    load_logs = BashOperator(
        task_id='load_logs',
        bash_command="""
        clickhouse-client --query="TRUNCATE TABLE logs_v2";
        clickhouse-client --query="INSERT INTO logs_v2 FORMAT TabSeparatedWithNames" < /tmp/logs_v2.csv
        """,
    )

 
    export_transactions >> load_transactions
    export_logs >> load_logs
