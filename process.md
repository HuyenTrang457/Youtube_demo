# 01_sql_basics
```bash
# provisioning mysql, and postgresql
docker-compose up -d
# destroy resources
docker-compose down

# use Makefile to provision resources
make up
# use Makefile to destroy resources
make down

# create table by using mysql_datasource.sql, psql_datasource.sql
```

# 02 Python basics
```bash
conda create -n aide python=3.10.6
conda activate aide
# conda env remove -n aide

conda install -c conda-forge pandas-profiling -y
```

# 03 Dagster basics

## Project structure
- Each data source is organized in each folder (e.g. brazil_ecom).
- Each folder is responsible for repository ETL of that data source (i.e. dockerized this folder).
- Run dagster gRPC server on specified port (e.g. 4000, 4001, etc). Refer here: https://grpc.io/
- Start dagster-daemon service for the long run.
- Start dagster-ui for data monitoring.
- Every operation in each pipeline must create unit-test for refactoring in the long run development.

## Start dagster
### 0. Dagster CLI
```bash
mkdir dagster_home
cd dagster_home
touch dagster.yaml
touch workspace.yaml

# dagster.yaml
run_coordinator:
  module: dagster.core.run_coordinator
  class: QueuedRunCoordinator
  config:
    max_concurrent_runs: 5
    tag_concurrency_limits:
      - key: "dagster/backfill"
        limit: 5

scheduler:
  module: dagster.core.scheduler
  class: DagsterDaemonScheduler
  config:
    max_catchup_runs: 5

# workspace.yaml
load_from:
  - python_file: repository.py

export DAGSTER_HOME=$PWD/dagster_home
dagster job execute -f job_example.py -c run_config.yaml
```
### 1. As a service
```bash
# CLI window 1
export DAGSTER_HOME=$PWD/dagster_home
dagster api grpc -p 4000 -f repository.py

# CLI window 2
export DAGSTER_HOME=$PWD/dagster_home
dagster-daemon run -w dagster_home/workspace.yaml

# CLI window 3
export DAGSTER_HOME=$PWD/dagster_home
dagit -p 3001 -w dagster_home/workspace.yaml

```
### 2. As docker compose all
```bash
# build new images
docker-compose build

# up and run
docker-compose up -d

# check Dagit
http://localhost:3000

docker-compose down
```

# 05 TDD basics
```bash
python -m pytest -vv --cov=examples tests/examples
```

# Dagster init full
```bash
# build all resources
make build

# up and run all services
make up

# destroy all services
make down

# check code format
make check
make lint

# test build services
make test

# create database for dagster
make to_psql
CREATE DATABASE db_dagster;
make down && make up
```
