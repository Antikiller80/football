DEBUG = False
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'football_bd',
        'USER': 'admin',
        'PASSWORD': 'v1z100p35',
        'HOST': 'localhost',
        'PORT': '',
    }
}