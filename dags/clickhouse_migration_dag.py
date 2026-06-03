from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

default_args = {
    "owner": "etl_user",
    "depends_on_past": False,
    "start_date": datetime(2026, 6, 3),
    'on_failure_callback': lambda context: print(f"Ошибка миграции: {context['exception']}"),
    "retries": 2,
    "retry_delay": timedelta(minutes=5)
}

with DAG(
        dag_id='clickhouse_migration_dag',
        default_args=default_args,
        schedule='50 23 * * *',
        catchup=False,
        max_active_tasks=3,
        max_active_runs=1,
        tags=["weather", "clickhouse", "migration", "postgres"],
        description="Data migration from postgres to clickhouse",
) as dag:

create_table = SQLExecuteQueryOperator(
    task_id='create_table',
    conn_id='main_clickhouse_connection',
    sql="clickhouse_migration_sql/table_creating.sql",
    dag=dag
)

moving_data_from_postgres_into_clickhouse = SQLExecuteQueryOperator(
    task_id='moving_data',
    conn_id='main_clickhouse_connection',
    sql='clickhouse_migration_sql/data_migration.sql',
    dag=dag
)

confirming_success = SQLExecuteQueryOperator(
    task_id='confirming_success',
    conn_id='main_clickhouse_connection',
    sql='clickhouse_migration_sql/task_completed.sql',
    dag=dag
)

create_table >> moving_data_from_postgres_into_clickhouse >> confirming_success