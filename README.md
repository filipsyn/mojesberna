# Moje Sběrna

## About

Web application for managing recycling center.

## Installation

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

# Runs docker containers
make up
```

### Manually

#### Setting up the environment

In the project root folder, there will be two files ending with `.env`.

- `container.example.env`
- `.example.env`

These two files are only example of real environment variables and should be good to go with prefilled values.

| "Real" file     | Example file            | Purpose                                           |
|-----------------|-------------------------|---------------------------------------------------|
| `.env`          | `.example.env`          | Provides environmental variables for the webapp   |
| `container.env` | `container.example.env` | Provides environment variables for database image | 

```shell
# Copies example files into "real" files
cp .container.example.env container.env
cp .example.env .env
```

#### Running docker containers

```shell
docker-compose up -d
```

Turning off docker containers.

```shell
docker-compose down 
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
