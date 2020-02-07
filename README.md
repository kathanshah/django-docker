# django-docker
Django Docker Boilerplace

#Start project App
docker-compose run app sh -c "django-admin.py startproject app ."

#Test Project
docker-compose run app sh -c "python manage.py test"

#Create New App
docker-compose run app sh -c "python manage.py startapp core"

#Make Migrations in App
docker-compose run app sh -c "python manage.py makemigrations core"