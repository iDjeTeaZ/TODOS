from flask import Flask, jsonify
from flask_cors import CORS
from flask_restful import Api
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint


from app import config


app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": config.CORS}})
api = Api(app)


from app import routes


if config.ENV == config.ENV_DEV:
	conf = config.DevelopmentConfig
elif config.ENV == config.ENV_PROD:
	conf = config.ProductionConfig
else:
	raise NameError(f'{config.ENV} is not a valid ENV')


@app.route('/swagger')
def swaggerController():
	swag = swagger(app)
	swag['info']['version'] = config.APP_VERSION
	swag['info']['title'] = config.API_NAME
	return jsonify(swag)

swaggerui_blueprint = get_swaggerui_blueprint(
	conf.SWAGGER_URL,
	conf.DATA_SWAGGER,
	config={
		'app_name': config.API_NAME
	}
)
app.register_blueprint(swaggerui_blueprint, url_prefix=conf.SWAGGER_URL)
