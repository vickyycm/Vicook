from models.database import get_db

#trae las recetas de la bbdd
def obtener_todas_las_recetas():
    db = get_db()
    return db.execute("SELECT * FROM recetas ORDER BY id").fetchall()

#trae id de receta o null
def obtener_receta_por_id(receta_id):
    db = get_db()
    return db.execute("SELECT * FROM recetas WHERE id = ?", (receta_id,)).fetchone()

#inserta la receta y da id
def crear_receta(nombre, descripcion, ingredientes, pasos):
    db = get_db()
    cursor = db.execute(
        "INSERT INTO recetas (nombre, descripcion, ingredientes, pasos) VALUES (?, ?, ?, ?)",
        (nombre, descripcion, ingredientes, pasos),
    )
    db.commit()
    return cursor.lastrowid