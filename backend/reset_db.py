import os
import configurations
import psycopg2 as Database

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fast_web_backend.settings')

configurations.setup()

from django.conf import settings

# Drop and re-create the database using django-extensions
conn_params = {
    'database': 'template1',
    'user': settings.DATABASES['default']['USER'],
    'password': settings.DATABASES['default']['PASSWORD'],
    'host': settings.DATABASES['default']['HOST'],
    'port': settings.DATABASES['default']['PORT']
}

connection = Database.connect(**conn_params)
connection.set_isolation_level(0)  # autocommit false
cursor = connection.cursor()

cursor.execute("""
    SELECT pg_terminate_backend(pg_stat_activity.pid)
    FROM pg_stat_activity
    WHERE pg_stat_activity.datname = '%s';
    """ % settings.DATABASES['default']['NAME'])

cursor.execute('''
    DROP DATABASE "%s";
    ''' % settings.DATABASES['default']['NAME'])

cursor.execute('''
    CREATE DATABASE "%s"
    WITH OWNER = "%s"
    ENCODING = 'UTF8';
''' % (settings.DATABASES['default']['NAME'], settings.DATABASES['default']['USER']))

connection.commit()
