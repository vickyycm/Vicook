import sqlite3
from models.database import get_db

def _row_to_dict(row):
    return dict(row) if row else None

#obtener todas las categorías con conteo de recetas
def obtener_todas_las_categorias():
    db = get_db()
    rows = db.execute("""
        SELECT c.id, c.nombre, c.descripcion, COUNT(r.id) as recetas_count
        FROM categorias c
        LEFT JOIN recetas r ON c.id = r.categoria_id
        GROUP BY c.id
        ORDER BY c.nombre
    """).fetchall()
    return [_row_to_dict(row) for row in rows]

#obtener categoría por id
def obtener_categoria_por_id(categoria_id):
    db = get_db()
    row = db.execute("SELECT * FROM categorias WHERE id = ?", (categoria_id,)).fetchone()
    return _row_to_dict(row)

#crear nueva categoría
def crear_categoria(nombre, descripcion):
    db = get_db()
    try:
        cursor = db.execute(
            "INSERT INTO categorias (nombre, descripcion) VALUES (?, ?)",
            (nombre, descripcion),
        )
        db.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        return None  

#actualizar categoría
def actualizar_categoria(categoria_id, nombre, descripcion):
    db = get_db()
    try:
        db.execute(
            "UPDATE categorias SET nombre = ?, descripcion = ? WHERE id = ?",
            (nombre, descripcion, categoria_id),
        )
        db.commit()
        return True
    except sqlite3.IntegrityError:
        return False  

#eliminar categoría si no tiene recetas asociadas
def eliminar_categoria(categoria_id):
    db = get_db()
    
#verificar si tiene recetas asociadas
    recetas_count = db.execute(
        "SELECT COUNT(*) as count FROM recetas WHERE categoria_id = ?",
        (categoria_id,)
    ).fetchone()["count"]
    
    if recetas_count > 0:
        return False  
    
    db.execute("DELETE FROM categorias WHERE id = ?", (categoria_id,))
    db.commit()
    return True

#contar recetas por categoría
def contar_recetas_por_categoria(categoria_id):
    db = get_db()
    result = db.execute(
        "SELECT COUNT(*) as count FROM recetas WHERE categoria_id = ?",
        (categoria_id,)
    ).fetchone()
    return result["count"] if result else 0
