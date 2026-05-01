from models.database import get_db

def _row_to_dict(row):
    return dict(row) if row else None

#trae las recetas de la bbdd con categoría
def obtener_todas_las_recetas():
    db = get_db()
    rows = db.execute("""
        SELECT r.*, c.nombre as categoria_nombre
        FROM recetas r
        LEFT JOIN categorias c ON r.categoria_id = c.id
        ORDER BY r.id
    """).fetchall()
    return [_row_to_dict(row) for row in rows]

#trae id de receta o null
def obtener_receta_por_id(receta_id):
    db = get_db()
    row = db.execute("""
        SELECT r.*, c.nombre as categoria_nombre
        FROM recetas r
        LEFT JOIN categorias c ON r.categoria_id = c.id
        WHERE r.id = ?
    """, (receta_id,)).fetchone()
    return _row_to_dict(row)

#inserta la receta y da id
def crear_receta(nombre, descripcion, ingredientes, pasos, categoria_id=None):
    db = get_db()
    cursor = db.execute(
        "INSERT INTO recetas (nombre, descripcion, ingredientes, pasos, categoria_id) VALUES (?, ?, ?, ?, ?)",
        (nombre, descripcion, ingredientes, pasos, categoria_id),
    )
    db.commit()
    return cursor.lastrowid

#actualizar receta existente
def actualizar_receta(receta_id, nombre, descripcion, ingredientes, pasos, categoria_id=None):
    db = get_db()
    db.execute(
        "UPDATE recetas SET nombre = ?, descripcion = ?, ingredientes = ?, pasos = ?, categoria_id = ? WHERE id = ?",
        (nombre, descripcion, ingredientes, pasos, categoria_id, receta_id),
    )
    db.commit()

#eliminar receta
def eliminar_receta(receta_id):
    db = get_db()
    db.execute("DELETE FROM recetas WHERE id = ?", (receta_id,))
    db.commit()

#obtener todas las categorías
def obtener_todas_las_categorias():
    db = get_db()
    rows = db.execute("SELECT * FROM categorias ORDER BY nombre").fetchall()
    return [_row_to_dict(row) for row in rows]

#obtener categoría por id
def obtener_categoria_por_id(categoria_id):
    db = get_db()
    row = db.execute("SELECT * FROM categorias WHERE id = ?", (categoria_id,)).fetchone()
    return _row_to_dict(row)

#obtener ingredientes de una receta con cantidad
def obtener_ingredientes_de_receta(receta_id):
    db = get_db()
    rows = db.execute("""
        SELECT i.id, i.nombre, i.unidad, ri.cantidad
        FROM receta_ingrediente ri
        JOIN ingredientes i ON ri.ingrediente_id = i.id
        WHERE ri.receta_id = ?
        ORDER BY i.nombre
    """, (receta_id,)).fetchall()
    return [_row_to_dict(row) for row in rows]