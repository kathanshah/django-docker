# django-docker
Django Docker Boilerplate

# Start project App
docker-compose run app sh -c "django-admin.py startproject app ."

# Test Project
docker-compose run --rm app sh -c "python manage.py test"

# Create New App
docker-compose run app sh -c "python manage.py startapp core"

# Make Migrations in App
docker-compose run app sh -c "python manage.py makemigrations core"

# Create Super User
docker-compose run app sh -c "python manage.py createsuperuser"

# Create New App - User
docker-compose run --rm app sh -c "python manage.py startapp user"

# Run the App via Docker
docker-compose up

# Build the Image
docker-compose build
