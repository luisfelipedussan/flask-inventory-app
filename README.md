# Flask Inventory Management System

A simple inventory management system built with Flask, MySQL, and Docker.

## Video Demo  
[https://youtu.be/oc_fBi8XJHc](https://youtu.be/oc_fBi8XJHc)


## Features

- CRUD operations for inventory items
- Responsive UI with Bootstrap 5
- Form validation
- MySQL database
- Docker containerization
- RESTful endpoints

## Prerequisites

- Docker
- Docker Compose
- Git

## Quick Start

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/flask-inventory-app.git
cd flask-inventory-app
```

2. **Build and start the containers**

```bash
docker-compose up --build
```

3. **Access the application**

Open your browser and navigate to `http://localhost:5000`

## API Endpoints (Manual Testing)

### Get all inventory items

```bash
curl http://localhost:5000/api/inventory
```

### Get a single inventory item

```bash
curl http://localhost:5000/api/inventory/1
```

### Create a new inventory item

```bash
curl -X POST http://localhost:5000/api/inventory \
  -H "Content-Type: application/json" \
  -d '{"name": "New Item", "quantity": 10}'
``` 

### Update an inventory item

```bash
curl -X PUT http://localhost:5000/api/inventory/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Updated Item", "quantity": 20}'
```

### Delete an inventory item

```bash
curl -X DELETE http://localhost:5000/api/inventory/1
```

## Database Setup

The application uses MySQL for the database. The database is created automatically when the containers are started.

## Docker Compose

The `docker-compose.yml` file defines the services for the application. The services include:

- `app`: The Flask application
- `db`: The MySQL database

The `app` service mounts the current directory to the `/app` directory in the container. The `db` service uses a MySQL image from Docker Hub.

## Configuration

The application configuration is stored in the `app/config.py` file. The configuration includes:

- `SECRET_KEY`: The secret key for the application
- `SQLALCHEMY_DATABASE_URI`: The database URI
- `SQLALCHEMY_POOL_SIZE`: The size of the connection pool
- `SQLALCHEMY_POOL_TIMEOUT`: The timeout for the connection pool
- `SQLALCHEMY_POOL_RECYCLE`: The number of seconds to recycle the connection pool

## Health Check

The application includes a health check endpoint that returns a 200 status code if the database is connected. The health check endpoint is `/health`.

## Debug Information

The application includes a debug information endpoint that returns information about the application. The debug information endpoint is `/debug`.

## API Documentation

The application includes Swagger documentation for the API. The Swagger documentation is available at `/api/docs`.

## Error Handling

The application includes error handling for the API. The error handling includes:

- 400 Bad Request: The request is invalid
- 404 Not Found: The resource is not found
- 500 Internal Server Error: The server encountered an error

