SECRET_KEY = 'django-insecure-lg*_uf6+p4e9z%x7f5(yuxw02c!ckn&%oqsx&zddfy6m3zluyh'
DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'test_db',
        'USER': 'forum_user',
        'PASSWORD': 'Ruslan-69',
        'HOST': '127.0.0.1',
        'PORT': 5432,
    }
}