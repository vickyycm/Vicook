from flask import Blueprint, render_template, request, redirect, url_for
from models.receta_model import (
    obtener_todas_las_recetas, obtener_receta_por_id, crear_receta,
    actualizar_receta, eliminar_receta, obtener_todas_las_categorias, obtener_ingredientes_de_receta
)

receta_bp = Blueprint("recetas", __name__)

#pone en lista todas las recetas
@receta_bp.route("/")
def index():
    recetas = obtener_todas_las_recetas()
    categorias = obtener_todas_las_categorias()
    return render_template("recetas/index.html", recetas=recetas, categorias=categorias)

#crear receta 
@receta_bp.route("/nueva", methods=["GET", "POST"])
def nueva_receta():
    categorias = obtener_todas_las_categorias()
    
    if request.method == "POST":
        nombre       = request.form.get("nombre", "").strip()
        descripcion  = request.form.get("descripcion", "").strip()
        ingredientes = request.form.get("ingredientes", "").strip()
        pasos        = request.form.get("pasos", "").strip()
        categoria_id = request.form.get("categoria_id", "").strip()

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
                                   datos_form=request.form, categorias=categorias)

        categoria_id_int = int(categoria_id) if categoria_id else None
        receta_id = crear_receta(nombre, descripcion, ingredientes, pasos, categoria_id_int)
        return redirect(url_for("recetas.detalle", receta_id=receta_id))

    return render_template("recetas/nueva.html", errores=[], datos_form={}, categorias=categorias)

#cada receta especifica
@receta_bp.route("/<int:receta_id>")
def detalle(receta_id):
    receta = obtener_receta_por_id(receta_id)
    if receta is None:
        return render_template("recetas/404.html"), 404
    ingredientes = obtener_ingredientes_de_receta(receta_id)
    return render_template("recetas/detalle.html", receta=receta, ingredientes=ingredientes)

#editar receta
@receta_bp.route("/<int:receta_id>/editar", methods=["GET", "POST"])
def editar_receta(receta_id):
    receta = obtener_receta_por_id(receta_id)
    if receta is None:
        return render_template("recetas/404.html"), 404
    
    categorias = obtener_todas_las_categorias()
    
    if request.method == "POST":
        nombre       = request.form.get("nombre", "").strip()
        descripcion  = request.form.get("descripcion", "").strip()
        ingredientes = request.form.get("ingredientes", "").strip()
        pasos        = request.form.get("pasos", "").strip()
        categoria_id = request.form.get("categoria_id", "").strip()

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
            return render_template("recetas/editar.html", errores=errores,
                                   datos_form=request.form, categorias=categorias, receta_id=receta_id)

        categoria_id_int = int(categoria_id) if categoria_id else None
        actualizar_receta(receta_id, nombre, descripcion, ingredientes, pasos, categoria_id_int)
        return redirect(url_for("recetas.detalle", receta_id=receta_id))

    return render_template("recetas/editar.html", errores=[], datos_form=receta, 
                         categorias=categorias, receta_id=receta_id)

#eliminar receta
@receta_bp.route("/<int:receta_id>/eliminar", methods=["POST"])
def eliminar_receta_route(receta_id):
    receta = obtener_receta_por_id(receta_id)
    if receta is None:
        return render_template("recetas/404.html"), 404
    
    eliminar_receta(receta_id)
    return redirect(url_for("recetas.index"))