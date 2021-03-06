from os import getenv

# Application configuration:
APP_PORT = int(getenv('STORE_PORT', 8000))


# Mongo db configuration:

MONGO_PORT = int(getenv('STORE_MONGO_PORT', 27017))
MONGO_HOST = getenv('STORE_MONGO_HOST', 'mongodb://localhost')


def MONGO_URL():
    return '%s:%s' % (MONGO_HOST, MONGO_PORT)


MONGO_DB_NAME = getenv('STORE_MONGO_DB_NAME', 'store')

# default configuration - maximum safety without replicas
MONGO_DB_WRITE_CONCERN = int(getenv('STORE_MONGO_DB_WRITE_CONCERN', 1))
MONGO_DB_JOURNAL = bool(getenv('STORE_MONGO_DB_JOURNAL', True))
MONGO_DB_TIMEOUT = int(getenv('STORE_MONGO_DB_TIMEOUT', 5000))
MONGO_FSYNC = bool(getenv('STORE_MONGO_FSYNC', False))
