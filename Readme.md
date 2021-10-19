# DevelopsToday [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

DevelopsToday is a test project with REST API on DRF. 

## Installation
Use the package manager pip to install all package from requirements.txt
```bash
pip3 install -r requirements.txt
```
> To install for develop change ***requirements.txt***
> ```text
> # This file is here because many Platforms as a Service look for
> # requirements.txt in the root directory of a project.
>
> -r requirements/development.txt
>```
## Settings
Create a ".env" file as in example "env.example"

Or

Write your own local env settings in config/settings.py

```python
env = environ.Env(
    DJANGO_DEBUG=(bool, False),
    DJANGO_SECRET_KEY=(str, 'CHANGEME!!!e8!1671ifpp362f9gbd3v@e($0_flznbb3fa2d4zg7zn@%yyk2'),
    DJANGO_ALLOWED_HOSTS=(list, []),
    DJANGO_DATABASE_URL=(str, 'postgres://USER:PASSWORD@HOST:PORT/database'),
)
```

## Migrate
Apply all migrations into your DB
```bash
python manage.py migrate
```
