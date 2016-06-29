from airflow import DAG
from datetime import datetime, timedelta
from operators.emr_spark_operator import EMRSparkOperator

default_args = {
    'owner': 'mdoglio@mozilla.com',
    'depends_on_past': True,
    'start_date': datetime(2016, 6, 27),
    'email': ['mdoglio@mozilla.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 3,
    'retry_delay': timedelta(minutes=30),
}

dag = DAG('crash_aggregates', default_args=default_args, schedule_interval='@daily')

t0 = EMRSparkOperator(task_id = "crash_aggregate_view",
                      job_name = "Crash Aggregate View",
                      instance_count = 9,
                      env = {"date": "{{ ds_nodash }}", "bucket": "{{ task.__class__.airflow_bucket }}"},
                      uri = "https://raw.githubusercontent.com/mozilla/telemetry-airflow/master/jobs/crash_aggregate_view.sh",
                      dag = dag)
