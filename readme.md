# Catalog System

## Description of the project

Basic catalog system to manage products, implemented via a REST API using Djagno Rest Framework.

- Product should have basic info such as sku, name, price and brand.

Two type of users:

- (i) admins to create / update / delete products and to create / update / delete other admins.
- (ii) anonymous users who can only retrieve products information but can't make changes.

Whenever an admin user makes a change in a product, we need to notify all other admins about the change, either via email or other mechanism.

It keeps track of the number of times every single product is queried by an anonymous user.

### Developer notes:

Some technical gotchas I found were the need of decoupling the email action out of the api due that It could affect in case the mailing service failed or could be out of service in this cases it could lead to the api to not respond as expected and thankfully to the use of a queue system if email sending were facing this problem it could give us the chance of fix the problem and not loss the pending mailing actions.

I list all achieved features:
- User, Product and Brand CRUD operations implemented via DRF APIViews.
- CRUD operations restricted as specified in "Description of the project".
- Async events on mailing operations.
- Contenerization and integration of a variety of services (listed below) via docker and docker compose.
- Intetrations tests added for User, Product and Brand endpoints.

## Architecture overview

- **App**: The core application, built with Django Rest Framework, handles the API endpoints, business logic, and data validation. It interacts with other components in the architecture.
- **Celery**: An asynchronous task queue used for handling background jobs and scheduling tasks. It allows the system to offload long-running processes, such as sending emails.
- **PostgreSQL**: Open-source relational database used for storing and managing the application's structured data.
- **Redis**: Facilitates communication between different components through its pub/sub capabilities, enhancing the application's performance and scalability.
- **Nginx**: Improves the overall reliability and scalability of the system by efficiently distributing incoming traffic and handling SSL termination.

![Project Diagram](./docs/diagram.png)

## Getting Started

Build project:

```sh
docker compose build
```

Start project:

```sh
docker compose up
```

Create superuser:

```sh
docker compose exec app python manage.py createsuperuser
```

Setup postman collection

![Setup Postman](./docs/postman-setup.png)

Setup DB Connection

![Setup Postman](./docs/db-connection.png)

## Other commands

Test commands:

```sh
docker compose exec app python manage.py test
```

Development commands:

```sh
docker compose exec app python manage.py makemigrations

docker compose exec app python manage.py migrate

docker compose exec app pip freeze > requirements.txt
```

Lint commands

```sh
docker compose exec app black .

docker compose exec app isort . --profile black
```
