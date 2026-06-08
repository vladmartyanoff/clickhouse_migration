from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow_clickhouse_plugin.operators.clickhouse import ClickHouseOperator

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

    create_database = ClickHouseOperator(
        task_id='create_database',
        clickhouse_conn_id='main_clickhouse_connection',
        sql="clickhouse_migration_sql/create_database.sql",
    )

    create_table = ClickHouseOperator(
        task_id='create_table',
        clickhouse_conn_id='main_clickhouse_connection',
        sql="clickhouse_migration_sql/table_creating.sql",
    )

    moving_data_from_postgres_into_clickhouse = ClickHouseOperator(
        task_id='moving_data',
        clickhouse_conn_id='main_clickhouse_connection',
        sql='clickhouse_migration_sql/data_migration.sql',
    )

    confirming_success = ClickHouseOperator(
        task_id='confirming_success',
        clickhouse_conn_id='main_clickhouse_connection',
        sql='clickhouse_migration_sql/task_completed.sql',
    )

    create_database >> create_table >> moving_data_from_postgres_into_clickhouse >> confirming_success