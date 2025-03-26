# Cart Service using Python FastAPI

[![Cart Service CI](https://github.com/vikas-bhapri/cart-service/actions/workflows/actions.yml/badge.svg)](https://github.com/vikas-bhapri/cart-service/actions/workflows/actions.yml)

This service provides endpoints for managing the shopping cart in an e-commerce application using Python FastAPI. It allows users to add, update, remove, and retrieve items in their cart.

Test the APIs for the cart service on [Cart Service API Documentation](https://yourdeploymenturl.com/redoc)

## Installation

### Prerequisites

- Python 3.6 or later
- pip
- Docker Desktop

### Environment Variables

To test the code locally, create a `.env` file and add the following environment variables:

```ini
DATABASE_CONNECTION_STRING=<Enter the connection string for the PostgreSQL database or the SQLite DB path>
```  

### Installing Dependencies

Run the following command to install the required dependencies:

```bash
pip install -r requirements.txt
```

### Running the Server Locally

To start the FastAPI server locally, execute:

```bash
uvicorn main:app --reload
```

The `--reload` flag enables automatic reloading of the application upon code changes. The server will be accessible at [http://localhost:8000](http://localhost:8000).

## Deployment

To deploy the application, build a Docker image and push it to a container registry such as [Docker Hub](https://hub.docker.com), [Azure Container Registry](https://azure.microsoft.com/en-us/products/container-registry), or [Amazon Elastic Container Registry](https://aws.amazon.com/ecr/).

### Building the Docker Image

Run the following command to build the Docker image:

```bash
docker build -t <image-name>:<tag> .
```

### Pushing the Image to a Container Registry

First, log in to the container registry:

```bash
docker login <registry-url> -u <username> -p <password>
```

> **Note:** The `registry-url` is not required when using Docker Hub.

Then, push the Docker image:

```bash
docker push <registry-url/username>/<image-name>:<tag>
```

### Deploying the Container

Once the image is pushed, deploy it using a container service such as:

- **Azure**: Azure Container Instances, Azure App Service
- **AWS**: Amazon ECS, AWS Fargate
- **Google Cloud**: Cloud Run, GKE

This ensures a scalable and managed deployment of your FastAPI service.

>**Note:** Make sure to set up the environment variables in the cloud to ensure the working of the app.
