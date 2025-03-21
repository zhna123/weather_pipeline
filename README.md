# Weather Pipeline

## Development - Local 
### Set up project
1. Create python virtual environment `python -m venv venv`, `source venv/bin/activate`
2. Install dependencies `pip install -r requirements.txt`
3. `pip freeze > requirements.txt`
### Set up postgre DB
1. use docker - edit `docer-compose.yml`
2. `docker-compose up -d`
3. verify `docker ps`
4. connect to DB
  - open shell in container `docker exec -it postgres_db bash`
  - `psql -U postgres -d weather`
  - optionally add pgadmin service and restart the services - access pgadmin at `http://localhost:5050`
### Create staging table for raw data from csv

#### Set up dbt
1. `pip install dbt-postgres`
2. setup/modify dbt folder structure
3. Configure dbt Connection to PostgreSQL
  - create/edit `~/.dbt/profiles.yml`
  - matching postgres in docker setup
  - Alternatively, reference .env variables to avoid hardcoding
4. Update Docker setup to mount the dbt folder - NOT DONE YET
5. test
  - start docker `docker-compose up -d`
  - `source venv/bin/activate`
  - test dbt connection `dbt debug`
  - generate models `dbt run`
#### dbt staging model - clean & organize data
1. Create a staging model (typically a view)
  - inside `dbt/models/staging/stg_weather.sql`
2. Define source
  - `models/staging/sources.yml`
3. Update dbt_project.yml to include models
4. Run and test staging model
  - cd into dbt folder
  - run `dbt run --select stg_weather`
  - test `dbt test --select stg_weather` - confirm model working correctly
### dbt intermediate model
#### Goal
* Calculate seasonal averages of temperatures for each city.
* Prepare the data for trend analysis (e.g., year-over-year changes).
* Create clean, aggregated data ready for the final star schema.
1. Create intermediate model
2. update dbt_project.yml to include this model
3. run dbt to create table
### testing - run dbt pipeline
* update schema.yml (testing and doc)
* use seed to create mock table/data for testing
  - create csv file in seeds folder(path specified in dbt_project.yml)
  - run `dbt seed`
* run dbt pipeline with `dbt build` (seed -> run -> test)
* generate doc (inside airflow container, make sure to mount the correct port)
  - `dbt docs generate` 
  - serve `dbt docs serve --port 8081 --host 0.0.0.0`

### Orchestration - airflow
#### Initialize and set up airflow
1. Add airflow to docker-compose (make sure credentials and DB match postgres)
2. set up `docker-compose up airflow-init` - only runs once for set up
3. start everything `docker-compose up -d`
4. log on to `localhost:8080`
#### Automate flow with DAG
* write the DAG file
* create custom airflow container to install dependencies 
#### Test DAG in airflow
##### key take aways
* Airflow needs proper path setup (sys.path.append(...) for importing scripts).
* Database connections should be modular (db_connection.py for reuse).
* Docker mounts must be correct (dbt/, scripts/, and data/ inside containers).
* Airflow DAGs should be structured cleanly (task dependencies, retries, logging).
* dbt needs the correct project and profiles path (--project-dir and --profiles-dir).



