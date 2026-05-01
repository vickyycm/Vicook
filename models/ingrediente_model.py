import sqlite3
from models.database import get_db

def _row_to_dict(row):
    return dict(row) if row else None

#obtener todos los ingredientes
def obtener_todos_los_ingredientes():
    db = get_db()
    rows = db.execute("""
        SELECT i.id, i.nombre, i.unidad, COUNT(ri.receta_id) as recetas_count
        FROM ingredientes i
        LEFT JOIN receta_ingrediente ri ON i.id = ri.ingrediente_id
        GROUP BY i.id
        ORDER BY i.nombre
    """).fetchall()
    return [_row_to_dict(row) for row in rows]

#obtener ingrediente por id
def obtener_ingrediente_por_id(ingrediente_id):
    db = get_db()
    row = db.execute("SELECT * FROM ingredientes WHERE id = ?", (ingrediente_id,)).fetchone()
    return _row_to_dict(row)

#crear nuevo ingrediente
def crear_ingrediente(nombre):
    db = get_db()
    try:
        cursor = db.execute(
            "INSERT INTO ingredientes (nombre) VALUES (?)",
            (nombre,),
        )
        db.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        return None

#actualizar ingrediente
def actualizar_ingrediente(ingrediente_id, nombre):
    db = get_db()
    try:
        db.execute(
            "UPDATE ingredientes SET nombre = ? WHERE id = ?",
            (nombre, ingrediente_id),
        )
        db.commit()
        return True
    except sqlite3.IntegrityError:
        return False

#eliminar ingrediente si no tiene recetas asociadas
def eliminar_ingrediente(ingrediente_id):
    db = get_db()
    
#verificar si tiene recetas asociadas
    recetas_count = db.execute(
        "SELECT COUNT(*) as count FROM receta_ingrediente WHERE ingrediente_id = ?",
        (ingrediente_id,)
    ).fetchone()["count"]
    
    if recetas_count > 0:
        return False
    
    db.execute("DELETE FROM ingredientes WHERE id = ?", (ingrediente_id,))
    db.commit()
    return True

#contar recetas por ingrediente
def contar_recetas_por_ingrediente(ingrediente_id):
    db = get_db()
    result = db.execute(
        "SELECT COUNT(*) as count FROM receta_ingrediente WHERE ingrediente_id = ?",
        (ingrediente_id,)
    ).fetchone()
    return result["count"] if result else 0

#obtener ingredientes de una receta con cantidad
def obtener_ingredientes_por_receta(receta_id):
    db = get_db()
    rows = db.execute("""
        SELECT i.id, i.nombre, ri.cantidad
        FROM receta_ingrediente ri
        JOIN ingredientes i ON ri.ingrediente_id = i.id
        WHERE ri.receta_id = ?
        ORDER BY i.nombre
    """, (receta_id,)).fetchall()
    return [_row_to_dict(row) for row in rows]
