from flask import Flask
from controller.path_controller import path_blueprint

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(path_blueprint, url_prefix="/api/v1")

if __name__ == "__main__":
    app.run(debug=True)
