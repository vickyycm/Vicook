from flask import Blueprint, render_template, request, redirect, url_for
from models.categoria_model import (
    obtener_todas_las_categorias, obtener_categoria_por_id, crear_categoria,
    actualizar_categoria, eliminar_categoria, contar_recetas_por_categoria
)

categoria_bp = Blueprint("categorias", __name__)

#listar todas las categorías
@categoria_bp.route("/")
def index():
    categorias = obtener_todas_las_categorias()
    return render_template("categorias/index.html", categorias=categorias)

#crear nueva categoría
@categoria_bp.route("/nueva", methods=["GET", "POST"])
def nueva_categoria():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        descripcion = request.form.get("descripcion", "").strip()

        errores = []
        if not nombre:
            errores.append("El nombre es obligatorio.")
        
        if errores:
            return render_template("categorias/nueva.html", errores=errores, datos_form=request.form)
        
        categoria_id = crear_categoria(nombre, descripcion)
        if categoria_id is None:
            errores.append("El nombre de la categoría ya existe.")
            return render_template("categorias/nueva.html", errores=errores, datos_form=request.form)
        
        return redirect(url_for("categorias.index"))
    
    return render_template("categorias/nueva.html", errores=[], datos_form={})

#editar categoría
@categoria_bp.route("/<int:categoria_id>/editar", methods=["GET", "POST"])
def editar_categoria(categoria_id):
    categoria = obtener_categoria_por_id(categoria_id)
    if categoria is None:
        return redirect(url_for("categorias.index", error="La categoría no existe."))
    
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        descripcion = request.form.get("descripcion", "").strip()

        errores = []
        if not nombre:
            errores.append("El nombre es obligatorio.")
        
        if errores:
            return render_template("categorias/editar.html", errores=errores, 
                                   datos_form=request.form, categoria_id=categoria_id)
        
        if not actualizar_categoria(categoria_id, nombre, descripcion):
            errores.append("El nombre de la categoría ya existe.")
            return render_template("categorias/editar.html", errores=errores, 
                                   datos_form=request.form, categoria_id=categoria_id)
        
        return redirect(url_for("categorias.index"))
    
    return render_template("categorias/editar.html", errores=[], 
                          datos_form=categoria, categoria_id=categoria_id)

#eliminar categoría
@categoria_bp.route("/<int:categoria_id>/eliminar", methods=["POST"])
def eliminar_categoria_route(categoria_id):
    categoria = obtener_categoria_por_id(categoria_id)
    if categoria is None:
        return redirect(url_for("categorias.index", error="La categoría no existe."))
    
    recetas_count = contar_recetas_por_categoria(categoria_id)
    if recetas_count > 0:
        return redirect(url_for("categorias.index", error=f"No se puede eliminar '{categoria['nombre']}' porque tiene {recetas_count} receta(s) asociada(s)."))
    
    eliminar_categoria(categoria_id)
    return redirect(url_for("categorias.index"))
