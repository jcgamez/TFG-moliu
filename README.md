# Moliu. Software for gross motor skills treatment

## Web application

This webapp is part of **Moliu** project. Its objective is the patients, specialists, activities, games and machine learning models management.

Managed entities:
* Patient: User who performs activities
* Specialist: Admin user responsible for managing Moliu software
* Activity: Interactive task proposed to patients
* Game: Activity performed by a patient
* Model: File that represents what was learned using machine learning techniques

In order to deploy this application you must create a .env file and set the following variables:
- DJANGO_SUPERUSER_USERNAME
- DJANGO_SUPERUSER_PASSWORD
- DJANGO_SUPERUSER_EMAIL
- SECRET_KEY
- DEBUG
- POSTGRES_DB_NAME
- POSTGRES_USER
- POSTGRES_PASSWORD
- POSTGRES_HOST
- PGADMIN_DEFAULT_EMAIL
- PGADMIN_DEFAULT_PASSWORD

However there are default values for this variables for working in development if you prefer.

To start moliuWeb for the first time execute `run.sh` script.