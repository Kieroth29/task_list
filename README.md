# task_list
Flask + Angular task list app, developed together with @lcaladoferreira. This project is still in development, meaning this README and the files might change.

## Dependencies
>Docker

## Installation
After cloning the repository, you will need to set environment variables for the PostgreSQL database, in the following format: 

	DB_PASSWORD=your_password
	DB_USER=your_user
	DB_NAME=your_db

The next step is 

Finally, navigate to the root folder and run the command:
`docker compose up -d`
A container will be created, running both API and database instances in the background.

## Ports
The Flask application will run under port 5000 by default, while the Postgres database will run under port 5434. You're free to change these ports to fit your needs, by editing the `docker-compose.yml` file, located on the project's root folder.