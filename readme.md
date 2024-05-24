# Catalog System

## Description of the task

Basic catalog system to manage products, implemented via a REST API using Djagno Rest Framework.

- Product should have basic info such as sku, name, price and brand.

Two type of users:

- (i) admins to create / update / delete products and to create / update / delete other admins.
- (ii) anonymous users who can only retrieve products information but can't make changes.

Whenever an admin user makes a change in a product (for example, if a price is adjusted), we need to notify all other admins about the change, either via email or other mechanism.

It keeps track of the number of times every single product is queried by an anonymous user.

## Commands

docker build -t catalog .

docker compose exec app black .

docker compose exec app pip freeze > requirements.txt

docker compose exec app isort . --profile black

docker compose exec app python manage.py makemigrations

docker compose exec app python manage.py migrate

docker compose exec app python manage.py startapp auth
