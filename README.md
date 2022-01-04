# exchangePortfolioAPI
Simple API for custom investing portfolio watch list.

## Run the project in local

1. Start the local DynamoDB Service
~~~
docker-compose up -d
~~~
2. Install the requirements
~~~
pip install requirements.txt
~~~
3. Start the fastAPI server
~~~
cd src
uvicorn main:app --reload --port 5000
~~~

## Validate code linter
~~~
cd src
flake8
~~~

## Run tests
To run tests and coverage report just use the pytest command
~~~
pytest
~~~
