**Development Environment**

1/ Build Postgres & Chroma databases: <br/>
`docker compose -f docker-compose.product.yml up --build -d`

2/<br/>
`poetry shell`

3/<br/>
`poetry install`

4/ Run (make sure this variable defined in all terminal tabs that you run following commands):<br/>
`export ENV_FILE=".env.dev"`<br/>

=> To check whether the os variable is set appropriately:<br/>
`echo $ENV_FILE`

5/ Run database migration scripts:<br/>
`alembic revision -m "message"`

`alembic upgrade head`

6/ Run main application:<br/>
`uvicorn app.main:main_app --reload`

7/ Run celery beat to monitor tasks:<br/>
`celery -A app.celery.celery_app worker --loglevel=info --concurrency=1 -P solo`

8/ Open Minio <br/>
`https://ehis.minio.console.codelearnit.io.vn`<br/>
