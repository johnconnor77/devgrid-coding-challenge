# FastAPI Weather Service

This project is a FastAPI application that collects data from the Open Weather API and stores it as JSON data. The service is built using FastAPI, SQLite, and Alembic.

## Table of Contents

- [Docker Installation](#docker-installation)
- [Running the FastAPI App](#running-the-fastapi-app)
- [Running Tests](#running-tests)
- [Running Coverage](#running-coverage)


## Docker Installation

To dockerize the FastAPI application, follow these steps:

1. Ensure you have Docker and Docker Compose installed on your machine. You can download them from [Docker's official website](https://www.docker.com/get-started).

2. Clone the repository:

   ```sh
   git clone https://github.com/johnconnor77/devgrid-coding-challenge.git
   cd fastapi-weather-service

3. Build the Docker image:

   ```sh
   docker-compose build

## Running the FastAPI App
To run the FastAPI application, follow these steps:

1. Start the Docker containers:

    ```sh
    docker-compose up
   
2. The FastAPI application will be available at http://localhost:8000.

3. To stop the application, use:

    ```sh
    docker-compose down
   
## Running Tests

To run all tests for the FastAPI application, follow these steps:

1. Start the Docker containers:

    ```sh
    docker-compose up --build
   
2. Run the tests:

    ```sh
    docker-compose exec -it fastapi_app pytest
   
3. Check the test results in the terminal.


## Running Coverage 

