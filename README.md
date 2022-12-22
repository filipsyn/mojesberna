# Moje Sběrna

## About

Web application for managing recycling center.

## Development setup

Prerequisites

- [Git](https://git-scm.com/downloads)
- [Docker](https://docs.docker.com/get-docker/)
- Preferably UNIX-based operating system
  or [Windows Subsystem for Linux](https://learn.microsoft.com/en-us/windows/wsl/install), because some things
  are written with UNIX in mind.

### Using GNU/Make (optional)

If you have [GNU/Make](https://www.gnu.org/software/make/#download) installed on your system (usually can be found on
UNIX-based systems or in WSL), you can use prepared scripts listed in [Makefile](Makefile).

```shell
# Installs the project
make install 

# Runs docker container and development server
make on
```

Be sure to check out `Makefile` for other useful scripts to use when developing.

### Manually

Set environmental variables

```shell
export FLASK_APP='src/app.py'
cp .example.env .env
```

Create and set-up virtual environment

```shell
python -m venv venv
source venv/bin/activate
pip install -r src/requirements.txt
```

Spin up docker database image

```shell
docker-compose up -d
```

Perform database migration

```shell
flask db migrate
flask db upgrade
```

After that, everything is ready to go. You can run application with:

```shell
flask run --port 8080 --host 0.0.0.0
```

## Development guidelines

[Here](docs/CONTRIBUTING.md) you can read more about some code guidelines.

## Used technologies

- Python
- Flask
- SQLAlchemy
- Docker
- PostgreSQL
- HTML
- CSS
