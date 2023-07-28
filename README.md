# SkyTrack
API service for airport management written on DRF

## Features

- JWT authenticated
- Admin panel /admin/
- Documentation is located at /api/doc/swagger/
- Creating airplanes with airplanes type
- Creating route and airports
- Creating crew and flights!
- Order system

## Installing using GitHub:
Install PostgresSQL and create db

1. Clone the repository:

```bash
git clone https://github.com/your-username/airport_api
```
2. Change to the project's directory:
```bash
cd airport_api
```
3. Сopy .env_sample file with your examples of env variables to your .env
file


4. Once you're in the desired directory, run the following command to create a virtual environment:
```bash
python -m venv venv
```
5. Activate the virtual environment:

On macOS and Linux:

```bash
source venv/bin/activate
```
On Windows:
```bash
venv\Scripts\activate
```

4. Install the dependencies

```bash
pip install -r requirements.txt
```

5. Set up the database:

Run the migrations

```bash
python manage.py migrate
```

6. Start the development server

```bash
python manage.py runserver
```

7. Access the website locally at http://localhost:8000.

## Run with Docker

Docker should be installed

```
docker-compose build
docker-compose up
```

## Getting access

- get access token via /api/user/token/ by 
```
email = user@test.com
password = user123123
```

or register you own user via /api/users/ and get access token
