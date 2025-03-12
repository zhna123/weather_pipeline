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