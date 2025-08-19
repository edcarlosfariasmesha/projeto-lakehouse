import os

import pendulum
from airflow.providers.papermill.operators.papermill import PapermillOperator
from airflow.sdk import Variable, dag


@dag(
    schedule="*/3 * * * *",
    start_date=pendulum.datetime(2025, 1, 1, tz="America/Maceio"),
    catchup=False,
    tags=["pyspark", "delta", "minio"],
)
def anp_serie_levantamento_precos():

    landing_anp_serie_levantamento_precos = PapermillOperator(
        task_id="landing_anp_serie_levantamento_precos",
        input_nb=os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "tasks",
            "landing",
            "src_lnd_anp_serie_levantamento_precos.ipynb",
        ),
        output_nb="/opt/airflow/logs/tasks/landing/src_lnd_anp_serie_levantamento_precos_{{ ts_nodash }}.ipynb",
        parameters={"minio_connection": Variable.get("minio_connection")},
    )

    bronze_anp_serie_levantamento_precos = PapermillOperator(
        task_id="bronze_anp_serie_levantamento_precos",
        input_nb=os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "tasks",
            "bronze",
            "lnd_brz_anp_serie_levantamento_precos.ipynb",
        ),
        output_nb="/opt/airflow/logs/tasks/bronze/lnd_brz_anp_serie_levantamento_precos_{{ ts_nodash }}.ipynb",
        parameters={"minio_connection": Variable.get("minio_connection")},
    )

    landing_anp_serie_levantamento_precos.set_downstream(
        bronze_anp_serie_levantamento_precos
    )


anp_serie_levantamento_precos()
