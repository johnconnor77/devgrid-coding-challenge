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

1. Start the Docker web container:

    ```sh
    docker-compose run -p 8000:8000 web
   
2. The FastAPI application will be available at http://localhost:8000/docs and you could test it right there.

![fast](https://github.com/user-attachments/assets/222bcb74-7c30-43e0-b17a-263c2160224a)

3. Example Video & Pictures

 3.1 Video recorded with jam: https://jam.dev/c/e746470c-cf3c-4f32-a4c3-2b8b202748c3


 3.2 Post Request http://localhost:8000/weather

 While Uploading the data

![1](https://github.com/user-attachments/assets/6402662f-f08a-4c57-bd81-115d3b0afdf2)

Process Finished


![3](https://github.com/user-attachments/assets/4f179a5e-cf6e-4e91-b5f4-184b234fad5a)

 3.3 Get Request  

 Fetch how many data is being uploaded

![2](https://github.com/user-attachments/assets/032545be-739b-439c-b1d7-6147fe5fdf27)

100% of data Uploaded


![4](https://github.com/user-attachments/assets/50207152-87ab-44be-90d1-9c2ae6bfd475)


3. To stop the application, use:

    ```sh
    docker-compose down



   
## Running Tests

To run all tests for the FastAPI application, follow these steps:

  
1. Run the tests command :

    ```sh
    docker-compose run tests
   
3. Check the test results in terminal


## Running Coverage 

1. Start the Docker containers:

    ```sh
    docker-compose run coverage

2. Check the test results in the /htmlcov/index.html
