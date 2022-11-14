# Moje Sběrna

## About

Web application for managing recycling center.

## Used technologies

- Python
- Flask
- SQLAlchemy
- Docker
- PostgreSQL
- HTML
- CSS

## Running the application

### Prerequisites

- [Git](https://git-scm.com/downloads)
- [Docker](https://docs.docker.com/get-docker/)
- Preferably UNIX-based operating system
  or [Windows Subsystem for Linux](https://learn.microsoft.com/en-us/windows/wsl/install), because some things
  are written with UNIX in mind.

### Downloading the project

```shell
git clone git@bitbucket.org:filipsynek/mojesberna.git

cd mojesberna/
```

### Using GNU/Make (optional)

#### Installation

If you have [GNU/Make](https://www.gnu.org/software/make/#download) installed on your system (usually can be found on
UNIX-based systems or in WSL), you can use install script
to set everything up for you.

```shell
make install
```

#### Running the project

After successful installation can spin-up the docker containers using

```shell
make up
```

### Manually

Even if you don't have GNU/Make installed, there's no need to worry. You just have to perform the project set-up
manually, step-by-step.

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

This project is completely "dockerized", so you only need to run the docker compose command.

```shell
docker-compose up -d
```

If you dont want to run the project anymore you can use the `down` argument for `docker-copose` command

```shell
docker-compose down --remove-orphans
```

## Development guidelines

[Here](docs/CONTRIBUTING.md) you can read more about some code guidelines.