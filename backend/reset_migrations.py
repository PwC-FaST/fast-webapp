import os
import glob

# Delete all the migration files and the data files
to_delete = set(glob.glob('*/migrations/*.py'))
to_delete = to_delete.union(set(glob.glob('*/migrations/*.pyc')))

# Do not delete the __init__.py files from the migrations folders
to_delete = to_delete.difference(set(glob.glob('*/migrations/__init__.py')))

# Delete the files
for f in to_delete:
    if os.path.isfile(f):
        print('Deleting', f)
        os.remove(f)
