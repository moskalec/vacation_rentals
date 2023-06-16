# Vacation rentals
## Startup
### Download source code
```git clone https://github.com/moskalec/vacation_rentals.git```
### Instal app
Enter folder
```cd vacation_rentals```

Run build
```docker-compose up -d```

Wait for launch...

Open in browser - [http://localhost:8000/rentals/filter/](http://localhost:8000/rentals/filter/), [swagger](http://localhost:8000/swagger/), [swagger.json](http://localhost:8000/swagger.json), [swagger.yaml](http://localhost:8000/swagger.yaml), [redoc](http://localhost:8000/redoc/)
## Run tests
```docker-compose run --rm web-app sh -c "python manage.py test vacation_rentals/tests"```

or use coverage

```docker-compose run --rm web-app sh -c "coverage run --source='vacation_rentals/' ./manage.py test vacation_rentals.tests"```

```docker-compose run --rm web-app sh -c "coverage report"```

```docker-compose run --rm web-app sh -c "coverage html"```

Open report in browseer .../vacation_rentals/service/htmlcov/index.html