from flask import Flask, redirect, url_for
from models.database import init_db, close_db
from controllers.receta_controller import receta_bp
from controllers.categoria_controller import categoria_bp

app = Flask(__name__, template_folder="views")


app.register_blueprint(receta_bp, url_prefix="")
app.register_blueprint(categoria_bp, url_prefix="/categorias")
app.teardown_appcontext(close_db)

#ruta raíz
@app.route("/")
def home():
    return redirect(url_for("recetas.index"))

#creacion de tablas y carga datos
if __name__ == "__main__":
    with app.app_context():
        init_db()          
    app.run(debug=True)