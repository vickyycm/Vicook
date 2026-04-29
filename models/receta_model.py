from models.database import get_db

def _row_to_dict(row):
    """Convierte sqlite3.Row a diccionario"""
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

#trae id de receta o null con categoría
def obtener_receta_por_id(receta_id):
    db = get_db()
    row = db.execute("""
        SELECT r.*, c.nombre as categoria_nombre, c.id as categoria_id_rel
        FROM recetas r
        LEFT JOIN categorias c ON r.categoria_id = c.id
        WHERE r.id = ?
    """, (receta_id,)).fetchone()
    return _row_to_dict(row)

#obtener todas las categorías
def obtener_todas_las_categorias():
    db = get_db()
    rows = db.execute("SELECT * FROM categorias ORDER BY nombre").fetchall()
    return [_row_to_dict(row) for row in rows]

#inserta la receta y da id
def crear_receta(nombre, descripcion, ingredientes, pasos, categoria_id=None):
    db = get_db()
    cursor = db.execute(
        "INSERT INTO recetas (nombre, descripcion, ingredientes, pasos, categoria_id) VALUES (?, ?, ?, ?, ?)",
        (nombre, descripcion, ingredientes, pasos, categoria_id),
    )
    db.commit()
    return cursor.lastrowid