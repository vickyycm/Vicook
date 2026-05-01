from flask import Blueprint, render_template, request, redirect, url_for
from models.receta_model import (
    obtener_todas_las_recetas, obtener_receta_por_id, crear_receta,
    actualizar_receta, eliminar_receta, obtener_todas_las_categorias, obtener_ingredientes_de_receta,
    eliminar_ingredientes_de_receta, agregar_ingrediente_a_receta
)
from models.ingrediente_model import obtener_todos_los_ingredientes

receta_bp = Blueprint("recetas", __name__)

@receta_bp.route("/")
def index():
    recetas = obtener_todas_las_recetas()
    categorias = obtener_todas_las_categorias()
    return render_template("recetas/index.html", recetas=recetas, categorias=categorias)

#crear receta 
@receta_bp.route("/nueva", methods=["GET", "POST"])
def nueva_receta():
    categorias = obtener_todas_las_categorias()
    todos_ingredientes = obtener_todos_los_ingredientes()
    
    if request.method == "POST":
        nombre       = request.form.get("nombre", "").strip()
        descripcion  = request.form.get("descripcion", "").strip()
        pasos        = request.form.get("pasos", "").strip()
        categoria_id = request.form.get("categoria_id", "").strip()
        
        ingrediente_ids = request.form.getlist("ingrediente_id[]")

        errores = []
        if not nombre:
            errores.append("El nombre es obligatorio.")
        if not descripcion:
            errores.append("La descripción es obligatoria.")
        if not pasos:
            errores.append("Los pasos de preparación son obligatorios.")

        if errores:
            return render_template("recetas/nueva.html", errores=errores, datos_form=request.form,
                                   categorias=categorias, todos_ingredientes=todos_ingredientes)

        categoria_id_int = int(categoria_id) if categoria_id else None
        receta_id = crear_receta(nombre, descripcion, pasos, categoria_id_int)
        
        for ingrediente_id in ingrediente_ids:
            if ingrediente_id:
                agregar_ingrediente_a_receta(receta_id, int(ingrediente_id), None)
        
        return redirect(url_for("recetas.detalle", receta_id=receta_id))

    return render_template("recetas/nueva.html", errores=[], datos_form={}, 
                          categorias=categorias, todos_ingredientes=todos_ingredientes)

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
    todos_ingredientes = obtener_todos_los_ingredientes()
    ingredientes_actuales = obtener_ingredientes_de_receta(receta_id)
    
    if request.method == "POST":
        nombre       = request.form.get("nombre", "").strip()
        descripcion  = request.form.get("descripcion", "").strip()
        pasos        = request.form.get("pasos", "").strip()
        categoria_id = request.form.get("categoria_id", "").strip()
        
        ingrediente_ids = request.form.getlist("ingrediente_id[]")

        errores = []
        if not nombre:
            errores.append("El nombre es obligatorio.")
        if not descripcion:
            errores.append("La descripción es obligatoria.")
        if not pasos:
            errores.append("Los pasos de preparación son obligatorios.")

        if errores:
            return render_template("recetas/editar.html", errores=errores, datos_form=request.form,
                                   categorias=categorias, todos_ingredientes=todos_ingredientes,
                                   ingredientes_actuales=ingredientes_actuales, receta_id=receta_id)

        categoria_id_int = int(categoria_id) if categoria_id else None
        actualizar_receta(receta_id, nombre, descripcion, pasos, categoria_id_int)
        
        eliminar_ingredientes_de_receta(receta_id)
        
        for ingrediente_id in ingrediente_ids:
            if ingrediente_id:
                agregar_ingrediente_a_receta(receta_id, int(ingrediente_id), None)
        
        return redirect(url_for("recetas.detalle", receta_id=receta_id))

    return render_template("recetas/editar.html", errores=[], datos_form=receta,
                          categorias=categorias, todos_ingredientes=todos_ingredientes,
                          ingredientes_actuales=ingredientes_actuales, receta_id=receta_id)

#eliminar receta
@receta_bp.route("/<int:receta_id>/eliminar", methods=["POST"])
def eliminar_receta_route(receta_id):
    receta = obtener_receta_por_id(receta_id)
    if receta is None:
        return render_template("recetas/404.html"), 404
    
    eliminar_receta(receta_id)
    return redirect(url_for("recetas.index"))