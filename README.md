BE_#2_-_Add_Dockerfile
## Clone the repository:

```
git clone https://github.com/VitalyBashkiser/Back-end.git
cd Backend
```

## Create a .env.dev file in the project root with the following content:

```
DEBUG=1
SECRET_KEY=django-insecure-#ljgyud+rtesq=)+@%oar80jaq)%=+@t19mzwm4i(8jt!h#!yy
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
```

## Make sure to replace your_secret_key with an actual Django secret key.

## Build and run the Docker container:

```
docker-compose up --build
```

This command will build the necessary Docker image and start the application.

## Open your web browser and go to http://127.0.0.1:8000 to access the application.








