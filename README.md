# FastAPI Weather Service

This project is a FastAPI application that collects data from the Open Weather API and stores it as JSON data. The service is built using FastAPI, SQLite, and Alembic.

## Table of Contents

- [Installation and Setup](#installation-and-setup)
- [Running the FastAPI App](#running-the-fastapi-app)
- [Running Tests](#running-tests)
- [Running Coverage](#running-coverage)


## Installation and Setup

1. Ensure you have Docker and Docker Compose installed on your machine. You can download them from [Docker's official website](https://www.docker.com/get-started).

2. Clone the repository:

   ```sh
   git clone https://github.com/johnconnor77/devgrid-coding-challenge.git

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
    docker-compose up
   
2. Run the tests command in other shell:

    ```sh
    docker-compose run tests
   
3. Check the test results in the /htmlcov/index.html


## Running Coverage 

1. Start the Docker containers:

    ```sh
    docker-compose up

2. Run the coverage command in other shell:

    ```sh
    docker-compose run coverage   


3. Check the test results in the /htmlcov/index.html