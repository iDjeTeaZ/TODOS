API_NAME = 'Todo'
APP_VERSION = '1.0'

MOCK_BDD = False
ENV_DEV = 'DEVELOPMENT'
ENV_PROD = 'PRODUCTION'
ENV = ENV_DEV
PRODUCTION_SERVER = '172.17.4.154'
PORT = 5001

CORS = '*'

SECRET = 'super_secret_key'
JWT_ALGO = 'HS256'

class BaseConfig:
    DEBUG = True
    SWAGGER_URL = '/api/docs'

class DevelopmentConfig(BaseConfig):
    DATA_SWAGGER = f'http://127.0.0.1:{PORT}/swagger'

class ProductionConfig(BaseConfig):
    DEBUG = False
    DATA_SWAGGER = f'http://{PRODUCTION_SERVER}:{PORT}/swagger'
