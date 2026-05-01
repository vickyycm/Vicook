from flask import Blueprint, render_template, request, redirect, url_for
from models.ingrediente_model import (
    obtener_todos_los_ingredientes, obtener_ingrediente_por_id, crear_ingrediente,
    actualizar_ingrediente, eliminar_ingrediente, contar_recetas_por_ingrediente
)

ingrediente_bp = Blueprint("ingredientes", __name__)

#lista todos los ingredientes
@ingrediente_bp.route("/")
def index():
    ingredientes = obtener_todos_los_ingredientes()
    return render_template("ingredientes/index.html", ingredientes=ingredientes)

#crear nuevo ingrediente
@ingrediente_bp.route("/nuevo", methods=["GET", "POST"])
def nuevo_ingrediente():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()

        errores = []
        if not nombre:
            errores.append("El nombre es obligatorio.")
        
        if errores:
            return render_template("ingredientes/nueva.html", errores=errores, datos_form=request.form)
        
        ingrediente_id = crear_ingrediente(nombre)
        if ingrediente_id is None:
            errores.append("El nombre del ingrediente ya existe.")
            return render_template("ingredientes/nueva.html", errores=errores, datos_form=request.form)
        
        return redirect(url_for("ingredientes.index"))
    
    return render_template("ingredientes/nueva.html", errores=[], datos_form={})

#editar ingrediente
@ingrediente_bp.route("/<int:ingrediente_id>/editar", methods=["GET", "POST"])
def editar_ingrediente(ingrediente_id):
    ingrediente = obtener_ingrediente_por_id(ingrediente_id)
    if ingrediente is None:
        return redirect(url_for("ingredientes.index", error="El ingrediente no existe."))
    
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()

        errores = []
        if not nombre:
            errores.append("El nombre es obligatorio.")
        
        if errores:
            return render_template("ingredientes/editar.html", errores=errores, 
                                   datos_form=request.form, ingrediente_id=ingrediente_id)
        
        if not actualizar_ingrediente(ingrediente_id, nombre):
            errores.append("El nombre del ingrediente ya existe.")
            return render_template("ingredientes/editar.html", errores=errores, 
                                   datos_form=request.form, ingrediente_id=ingrediente_id)
        
        return redirect(url_for("ingredientes.index"))
    
    return render_template("ingredientes/editar.html", errores=[], 
                          datos_form=ingrediente, ingrediente_id=ingrediente_id)

#eliminar ingrediene
@ingrediente_bp.route("/<int:ingrediente_id>/eliminar", methods=["POST"])
def eliminar_ingrediente_route(ingrediente_id):
    ingrediente = obtener_ingrediente_por_id(ingrediente_id)
    if ingrediente is None:
        return redirect(url_for("ingredientes.index", error="El ingrediente no existe."))
    
    recetas_count = contar_recetas_por_ingrediente(ingrediente_id)
    if recetas_count > 0:
        return redirect(url_for("ingredientes.index", error=f"No se puede eliminar '{ingrediente['nombre']}' porque está asociado a {recetas_count} receta(s)."))
    
    eliminar_ingrediente(ingrediente_id)
    return redirect(url_for("ingredientes.index"))
