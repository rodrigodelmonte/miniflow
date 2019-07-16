from airflow import DAG
from datetime import datetime
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2019, 1, 4),
    'retries': 0,
}

dag = DAG(
      dag_id='kubernetes_dag',
      default_args=default_args,
      schedule_interval='*/10 * * * *',
      catchup = False)

kubernetes_dag = KubernetesPodOperator(namespace='airflow',
                          image="python:3.7",
                          cmds=["python","-c"],
                          arguments=["print('hello world')"],
                          name="kubernetes-dag",
                          task_id="kubernetes_dag",
                          is_delete_operator_pod=True,
                          get_logs=True,
                          dag=dag
                          )

kubernetes_dag
