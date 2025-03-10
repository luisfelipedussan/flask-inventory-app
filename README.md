# Flask Inventory Management System

A comprehensive inventory management system built with Flask, MySQL, and Docker.

## Project Structure

```
flask-inventory-app/
├── app/                      # Application package
│   ├── __init__.py          # Flask app initialization
│   ├── config.py            # Configuration settings
│   ├── models/              # Database models
│   │   └── inventory.py     # Inventory model definition
│   ├── routes/              # Route handlers
│   │   └── inventory.py     # Inventory routes
│   └── templates/           # Jinja2 templates
│       ├── base.html        # Base template
│       ├── index.html       # Inventory list view
│       ├── add.html         # Add item form
│       └── edit.html        # Edit item form
├── Dockerfile               # Docker image definition
├── docker-compose.yml       # Docker services config
└── run.py                   # Application entry point
```

## 🎥 Video Demo 
[https://youtu.be/oc_fBi8XJHc](https://youtu.be/oc_fBi8XJHc)


## Features

- **CRUD Operations**
  - Create: Add new inventory items
  - Read: View all items in a responsive table
  - Update: Edit existing items
  - Delete: Remove items from inventory

- **Data Validation**
  - Client-side validation using HTML5 and JavaScript
  - Server-side validation for all inputs
  - MAC address format validation
  - Unique constraints on MAC and serial numbers

- **User Interface**
  - Responsive Bootstrap 5 design
  - Form validation feedback
  - Flash messages for operations
  - Confirmation dialogs for deletion

- **Error Handling**
  - Comprehensive error messages
  - Database transaction management
  - Logging of all operations
  - User-friendly error displays

## Prerequisites

- Docker
- Docker Compose
- Git

## Quick Start

1. **Clone the repository**

```bash
git clone https://github.com/luisfelipedussan/flask-inventory-app.git
cd flask-inventory-app
```

2. **Build and start the containers**

```bash
docker-compose up --build
```

3. **Access the application**

Open your browser and navigate to `http://localhost:5001`

# API Endpoints 

- Main page displaying a list of all elements in the database.
- /add: Page for adding a new element to the database.
- /edit/<id>: Page for editing an existing element in the database, where <id> is the
element's unique identifier.
- /delete/<id>: Route for deleting an element from the database.

## Manual Testing

### Get all inventory items

```bash
curl http://localhost:5001/api/inventory
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

