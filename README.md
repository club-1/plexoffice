# PlexOffice

A micro backoffice to manage some Plex stuffs, extensively using Django admin.

![plexoffice admin](docs/plexoffice-admin.png)

## Get started

To run the project.

### Install

```bash

# create virtualenv in the env dir then activate it
virtualenv env
. env/bin/activate

# copy sample .example.env file and edit Plex credentials
cp .example.env .env
nano .env
```

### Build

```bash
# install dependencies
pip install -r requirements.txt
# update database schema
./manage.py migrate
# collect static files (not needed for development)
./manage.py collectstatic --noinput
# generate translation files
./manage.py compilemessages -v0
```

### Run

    ./manage.py runserver

## Develop

Some tips about developing this app.

### Translate

Generate the translation files:

    ./manage.py makemessages -a

## Deploy
Edit `.env` file to give it safe values for productions:
1.  change the `SECRET_KEY`
2.  set `DEBUG` to `False`
3.  set `ALLOWED_HOSTS` value (coma separated list)
4.  use another `DATABASE_URL` than sqlite if possible (see [django-environ docs](https://github.com/joke2k/django-environ#tips))

At each new deployment, repeat the [build steps](#build).

### With Apache2

#### Install mod_wsgi

```bash
# Debian
sudo apt-get install libapache2-mod-wsgi
sudo systemctl restart apache2
```

#### Exemple site vhost

```apacheconf
<VirtualHost *:80>

    # ...
    # Your classic vhost conf
    # ...

    ##################################
    ### Conf for Django Plexoffice ###
    ##################################

    # Wsgi module conf
    <IfModule mod_wsgi.c>
        WSGIDaemonProcess plexoffice python-home={virtual-env-dir} python-path={plexoffice-root-dir} user={user-name} group={group-name}
        WSGIProcessGroup plexoffice
        WSGIScriptAlias {url-path} {plexoffice-root-dir}/plexoffice/wsgi.py process-group=plexoffice
    </IfModule>

    # Authorize access to static files' dir
    Alias {url-path}/static/ {plexoffice-root-dir}/collect/
    <Directory {plexoffice-root-dir}/collect>
        Require all granted
    </Directory>

    # Authorize acces to django launch script
    <Directory {plexoffice-root-dir}/>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>
</VirtualHost>
```
