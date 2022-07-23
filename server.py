from flask_migrate import Migrate
from flask_cors import CORS
from app.server_config import bp, api
from app import create_application, db
from configs import *

app = create_application(os.getenv('CRUD_SERVER_ENV') or 'prod')
app.url_map.strict_slashes = False
CORS(app, resources={r"/serve/*": {"origins": "*"}})
app.register_blueprint(bp)
with app.app_context():
    db.create_all()
app.app_context().push()
migrate = Migrate(app, db)