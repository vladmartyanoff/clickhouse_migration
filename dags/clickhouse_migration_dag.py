from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

default_args = {
    "owner": "etl_user",
    "depends_on_past": False,
    "start_date": datetime(2026, 6, 2),
    "retries": 2,
    "retry_delay": timedelta(minutes=5)
}

dag = DAG('weather_migration_to_clickhouse', default_args=default_args, schedule='50 23 * * *', catchup=False, max_active_tasks=3, max_active_runs=1, tags=["weather", "clickhouse", "migration"], description="Daily max temperature per city")

create_table = SQLExecuteQueryOperator(
    task_id='create_table',
    conn_id='main_clickhouse_connection',
    sql="clickhouse_migration_sql/table_creating.sql",
    dag=dag
)