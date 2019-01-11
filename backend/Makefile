# Management commands for the Django server

# All commands expect the DJANGO_CONFIGURATION environment variable to
# be set to either Dev or Prod
# eg:
#    DJANGO_CONFIGURATION=Dev make start
# or alternatively:
#    export DJANGO_CONFIGURATION=Dev
#    make start

# Start the development server
start:
	set -o allexport && source dev.env && source secret.env && set +o allexport && \
	pipenv run python manage.py runserver 0.0.0.0:8002

# Build migrations
migrations:
	pipenv run python manage.py makemigrations

# Apply migrations
migrate:
	pipenv run python manage.py migrate

# Collect static files, including farmer_mobile_app build
collectstatic:
	pipenv run python manage.py collectstatic --noinput --clear

# Delete all the migrations
resetmigrations:
	pipenv run python reset_migrations.py

# Destroy and re-create the database
resetdb:
	pipenv run python reset_db.py

# Load the initial data from the init/ folder (fixtures and media)
loadinit:
	pipenv run python load_init.py

# Fully resets the dev environment
resetall: resetmigrations resetdb migrations migrate collectstatic loadinit

# Dump the GraphQL schema to the fast_web_backend/schema.json file
schema:
	pipenv run python manage.py graphql_schema --indent 4 --out fast_web_backend/schema.json
	pipenv run python manage.py graphql_schema --indent 4 --out ../farmer_mobile_app/src/apollo/schema.json

# Generate a png of the Django data model
models:
	pipenv run python manage.py graph_models -a -g -o fast_models.png
