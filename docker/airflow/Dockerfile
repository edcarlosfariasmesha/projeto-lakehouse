FROM apache/airflow:3.0.2
COPY requirements.txt /
RUN pip install --no-cache-dir "apache-airflow==3.0.2" -r /requirements.txt

USER root

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         openjdk-17-jdk-headless \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

USER airflow

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64