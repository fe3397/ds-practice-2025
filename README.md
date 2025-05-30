# Distributed Systems @ University of Tartu

This repository contains the initial code for the practice sessions of the Distributed Systems course at the University of Tartu.

## Getting started

### Overview

The code consists of multiple services. Each service is located in a separate folder. The `frontend` service folder contains a Dockerfile and the code for an example bookstore application. Each backend service folder (e.g. `orchestrator` or `fraud_detection`) contains a Dockerfile, a requirements.txt file and the source code of the service. During the practice sessions, you will implement the missing functionality in these backend services, or extend the backend with new services.

There is also a `utils` folder that contains some helper code or specifications that are used by multiple services. Check the `utils` folder for more information.

### Running the code with Docker Compose [recommended]

To run the code, you need to clone this repository, make sure you have Docker and Docker Compose installed, and run the following command in the root folder of the repository:

```bash
docker compose up
```

This will start the system with the multiple services. Each service will be restarted automatically when you make changes to the code, so you don't have to restart the system manually while developing. If you want to know how the services are started and configured, check the `docker-compose.yaml` file.

The checkpoint evaluations will be done using the code that is started with Docker Compose, so make sure that your code works with Docker Compose.

If, for some reason, changes to the code are not reflected, try to force rebuilding the Docker images with the following command:

```bash
docker compose up --build
```

### Run the code locally

Even though you can run the code locally, it is recommended to use Docker and Docker Compose to run the code. This way you don't have to install any dependencies locally and you can easily run the code on any platform.

If you want to run the code locally, you need to install the following dependencies:

backend services:
- Python 3.8 or newer
- pip
- [grpcio-tools](https://grpc.io/docs/languages/python/quickstart/)
- requirements.txt dependencies from each service

frontend service:
- It's a simple static HTML page, you can open `frontend/src/index.html` in your browser.

And then run each service individually.

Diagrams

![system](https://github.com/user-attachments/assets/65655245-c322-4c90-9c49-989305d24f75)


![architecture](https://github.com/user-attachments/assets/57414e7c-ee1a-473a-9c54-cb96f2fd21ac)

![ms2vectorclock](https://github.com/user-attachments/assets/47533398-3675-46cd-8e09-6c38d25c1916)

![consistency_protocol](https://github.com/user-attachments/assets/b7e169b4-6d66-4dea-bba3-860e107d2422)

![distributed_commit](https://github.com/user-attachments/assets/e3e11ce3-2e04-4100-a7e5-38774e261943)

![book_system](https://github.com/user-attachments/assets/c87754f8-03c3-44cd-a0e5-068a67f3f91f)

