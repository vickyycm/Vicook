from flask import Flask
from models.database import init_db
from controllers.receta_controller import receta_bp

app = Flask(__name__, template_folder="views")


app.register_blueprint(receta_bp)

#creacion de tablas y carga datos
if __name__ == "__main__":
    with app.app_context():
        init_db()          
    app.run(debug=True)