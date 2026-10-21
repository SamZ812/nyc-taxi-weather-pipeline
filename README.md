# NYC Taxi + Weather DE Project

Using this project with the purpose of teaching myself the technologies I don't typically get to use at work with hopes of becoming a better Data Engineer who can understand limitations of each step of a workflow. I will be focused on learning the following technologies and introducing bugs on purpose via Claude Code throughout the process to ensure I have visiblity into true issues that may arise with the technologies:

1. Linux
2. Docker
3. Python for ingestion
4. MinIO/S3
5. PySpark
6. dbt models + test
7. Postgres
8. Metabase
9. Airflow for orchestration

## Running locally

Requires Docker with Compose.

```bash
cp .env.example .env      # then edit the values
docker compose up -d
docker compose ps         # wait for "healthy"
```
