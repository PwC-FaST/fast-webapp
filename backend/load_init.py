import os
import shutil
import glob
import configurations
import yaml

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fast_web_backend.settings')
configurations.setup()

from django.conf import settings
from django.core.management import call_command
from core.models import FaSTUser, Country

# Load initial fixtures
FIXTURES_1 = [
    'init/fixtures/admin-interface/admin_interface_theme_FaST.json',
    'init/fixtures/core/countries.yaml',
]

for f in FIXTURES_1:
    call_command('loaddata', f, verbosity=2)

# Create users
with open('init/fixtures/core/fast_users.yaml') as f:
    USERS_TO_CREATE = yaml.load(f)

DEFAULT_PASSWORD = os.getenv('FAST_WEBAPP_DEFAULT_DJANGO_PASSWORD')

for user_to_create in USERS_TO_CREATE:
    
    user_id = user_to_create['pk']
    username = user_to_create['fields']['username']

    country = Country.objects.get(pk=user_to_create['fields']['country']) \
        if user_to_create['fields']['country'] is not None else None

    first_name = user_to_create['fields'].get('first_name', None)
    last_name = user_to_create['fields'].get('last_name', None)
    email = user_to_create['fields'].get('email', None)

    is_staff = user_to_create['fields'].get('is_staff', False)
    is_active = user_to_create['fields'].get('is_active', True)
    is_superuser = user_to_create['fields'].get('is_superuser', False)

    print('Creating user', username, DEFAULT_PASSWORD, is_staff, is_superuser, is_active)

    FaSTUser.objects.create_user(id=user_id,
                                 username=username,
                                 password=DEFAULT_PASSWORD,
                                 country=country,
                                 first_name=first_name,
                                 last_name=last_name,
                                 email=email,
                                 is_staff=is_staff,
                                 is_active=is_active,
                                 is_superuser=is_superuser)

# Load more fixtures
FIXTURES_2 = [
    'init/fixtures/messaging/threads.yaml',
    'init/fixtures/messaging/contacts.yaml',
    'init/fixtures/additional_services/subscription_types.yaml',
    'init/fixtures/additional_services/providers',
    'init/fixtures/additional_services/services',
    'init/fixtures/farming/crop_species.yaml',
    'init/fixtures/farming/livestock_species.yaml',
    'init/fixtures/farming/farming_commitments.yaml',
    'init/fixtures/farming/farmers.yaml',
    'init/fixtures/farming/farms/domaine_de_fortis.yaml',
    'init/fixtures/farming/farms/iglesia_de_san_pedro.yaml',
    'init/fixtures/nmp/plans/domaine_de_fortis.yaml',
    'init/fixtures/nmp/plans/iglesia_de_san_pedro.yaml'
]

for f in FIXTURES_2:
    call_command('loaddata', f, verbosity=2)

# Delete  and reload all media files
if os.path.exists(settings.MEDIA_ROOT) and os.path.isdir(settings.MEDIA_ROOT):
    for f in glob.glob(os.path.join(settings.MEDIA_ROOT, '*')):
        print('Removing %s...' % f)
        if os.path.isfile(f):
            os.unlink(f)
        elif os.path.isdir(f):
            shutil.rmtree(f)
    for f in os.listdir('init/media'):
        s = os.path.join('init/media', f)
        d = os.path.join(settings.MEDIA_ROOT, f)
        print('Copying %s...' % s)
        if os.path.isdir(s):
            shutil.copytree(s, d, False, None)
        else:
            shutil.copy2(s, d)
