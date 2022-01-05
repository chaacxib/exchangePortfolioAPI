# exchangePortfolioAPI
Simple API for custom investing portfolio watch list.

## Prerequisits
A Yahoo Finance API Key is needed to use this project, one can be obtained here [Link](https://rapidapi.com/apidojo/api/yh-finance/)

## Run the project in local
1. Copy the `.env` file example
~~~
cp .env.example .env
~~~
2. Open the .env file and replace the value of `YH_FINANCE_API_KEY` with your Yahoo Finance API Key

3. Start the local DynamoDB Service
~~~
docker-compose up -d
~~~
4. Install the requirements
~~~
pip install requirements.txt
~~~
5. Start the fastAPI server
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

## Deployment steps
1. Create the Lambda layer package with the following command
~~~
docker run -v "$PWD":/var/task "public.ecr.aws/sam/build-python3.9" /bin/sh -c "pip install -r requirements.txt -t python/lib/python3.9/site-packages/; exit"
~~~
2. Create a .zip file archive for your layer
~~~
zip -r exchangePortfolioAPILayer.zip python > /dev/null
~~~
3. Update the layer on AWS [Reference](https://aws.amazon.com/premiumsupport/knowledge-center/lambda-layer-simulated-docker/)

4. Create a `.zip` file with your code
~~~
zip -r exchangePortfolioAPI.zip src -x '*__pycache__*' '*tests*' '*tox.ini'
~~~