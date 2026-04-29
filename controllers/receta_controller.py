from flask import Blueprint, render_template, request, redirect, url_for
from models.receta_model import obtener_todas_las_recetas, obtener_receta_por_id, crear_receta, obtener_todas_las_categorias

receta_bp = Blueprint("recetas", __name__)

#pone en lista todas las recetas
@receta_bp.route("/")
def index():
    recetas = obtener_todas_las_recetas()
    categorias = obtener_todas_las_categorias()
    return render_template("recetas/index.html", recetas=recetas, categorias=categorias)

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
        categoria_id = request.form.get("categoria_id", None)
        
        # Convertir a None si es vacío o "null"
        if not categoria_id or categoria_id == "null":
            categoria_id = None
        else:
            categoria_id = int(categoria_id)

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
            categorias = obtener_todas_las_categorias()
            return render_template("recetas/nueva.html", errores=errores,
                                   datos_form=request.form, categorias=categorias)

        receta_id = crear_receta(nombre, descripcion, ingredientes, pasos, categoria_id)
        return redirect(url_for("recetas.detalle", receta_id=receta_id))

    categorias = obtener_todas_las_categorias()
    return render_template("recetas/nueva.html", errores=[], datos_form={}, categorias=categorias)