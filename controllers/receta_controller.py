from flask import Blueprint, render_template, request, redirect, url_for
from models.receta_model import obtener_todas_las_recetas, obtener_receta_por_id, crear_receta

receta_bp = Blueprint("recetas", __name__)

#pone en lista todas las recetas
@receta_bp.route("/")
def index():
    recetas = obtener_todas_las_recetas()
    return render_template("recetas/index.html", recetas=recetas)

#cada receta especifica
@receta_bp.route("/receta/<int:receta_id>")
def detalle(receta_id):
    receta = obtener_receta_por_id(receta_id)
    if receta is None:
        return render_template("recetas/404.html"), 404
    return render_template("recetas/detalle.html", receta=receta)

#crear receta
@receta_bp.route("/receta/nueva", methods=["GET", "POST"])
def nueva_receta():
    if request.method == "POST":
        nombre       = request.form.get("nombre", "").strip()
        descripcion  = request.form.get("descripcion", "").strip()
        ingredientes = request.form.get("ingredientes", "").strip()
        pasos        = request.form.get("pasos", "").strip()

        errores = []
        if not nombre:
            errores.append("El nombre es obligatorio.")
        if not descripcion:
            errores.append("La descripción es obligatoria.")
        if not ingredientes:
            errores.append("Los ingredientes son obligatorios.")
        if not pasos:
            errores.append("Los pasos de preparación son obligatorios.")

        if errores:
            return render_template("recetas/nueva.html", errores=errores,
                                   datos_form=request.form)

        receta_id = crear_receta(nombre, descripcion, ingredientes, pasos)
        return redirect(url_for("recetas.detalle", receta_id=receta_id))

    return render_template("recetas/nueva.html", errores=[], datos_form={})