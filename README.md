# exchangePortfolioAPI
Simple API for custom investing portfolio watch list.

## Run the project in local

1. Start the local DynamoDB Service
~~~
docker-compose up -d
~~~
2. Start the fastAPI server
~~~
cd src
uvicorn main:app --reload --port 5000
~~~
