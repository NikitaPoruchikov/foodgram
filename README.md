# Foodgram - Recipe Assistant 🍲
Foodgram is an online service for sharing recipes. Users can create recipes, add them to favorites, follow other authors, and create a shopping list for convenient meal planning.

For easy navigation, recipes are tagged with Tags.

## Technologies Used
![Python](https://img.shields.io/badge/Python-3.9-3670A0?style=for-the-badge&logo=python&logoColor=yellow&labelColor=black)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white&labelColor=black)
![Nginx](https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white&labelColor=black)
![Gunicorn](https://img.shields.io/badge/Gunicorn-298729?style=for-the-badge&logo=gunicorn&logoColor=white&labelColor=black)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white&labelColor=black)
![DjangoREST](https://img.shields.io/badge/DRF-ff1709?style=for-the-badge&logo=django&logoColor=white&labelColor=black)


### Deployment Instructions on a Remote Server:
Clone the project repository:


```sh
git clone https://github.com/NikitaPoruchikov/foodgram.git
Connect to the remote server.
```
Install Docker on the server:

```sh
apt install docker.io
Install Docker Compose:
```
```sh
curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
Edit the Nginx server configuration:
```
Modify the server_name in the ../infra/nginx.conf file to match the IP address of your server.

Copy the docker-compose.yml and nginx.conf files from ../infra/ to the server:

```sh
scp docker-compose.yml <username>@<host>:/home/<username>/docker-compose.yml
scp nginx.conf <username>@<host>:/home/<username>/nginx.conf
Create environment variables (as specified in ../infra/env.example) and add them to GitHub Actions Secrets.
```
Set up and activate a virtual environment (for Windows):

```sh

python -m venv venv
source venv/Scripts/activate
python -m pip install --upgrade pip
Run the application in containers:
```
```sh

docker-compose up -d --build
Apply migrations:
```
```sh

docker-compose exec backend python manage.py migrate
Create a superuser:
```
```sh

docker-compose exec backend python manage.py createsuperuser
Collect static files:
```
```sh

docker-compose exec backend python manage.py collectstatic --no-input
Load test data:
```
```sh
docker-compose exec backend python manage.py load_ingredients
docker compose exec backend python manage.py import_tags
To stop the application:
```
```sh
docker-compose down -v
Running Locally:
Clone the repository:
```
```sh
git clone https://github.com/NikitaPoruchikov/foodgram.git
Rename example.env in the ../infra/ folder to .env and fill it with your settings:
```
```sh
POSTGRES_DB=<database_name>
POSTGRES_USER=<database_user>
POSTGRES_PASSWORD=<database_password>
```
After starting, the project is accessible at http://localhost/, and documentation can be found at http://localhost/api/docs/.

Project is deployed at https://foodgrami.zapto.org/

Admin panel access:

plaintext
https://foodgrami.zapto.org/admin
login: rev20240@gmail.com
pass: asd123
### Author
Nikita Poruchikov