import sqlite3
from flask import g

DB_PATH = "vicook.db"


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row   
    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recetas (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre      TEXT    NOT NULL,
            descripcion TEXT    NOT NULL,
            ingredientes TEXT   NOT NULL,
            pasos       TEXT    NOT NULL
        )
    """)
    conn.commit()

#solo insertar datos de ejemplo si la tabla está vacía
    if cursor.execute("SELECT COUNT(*) FROM recetas").fetchone()[0] == 0:
        recetas_ejemplo = [
            (
                "Pasta al tomate",
                "Un clásico italiano, rápido y delicioso.",
                "400g de pasta\n2 tazas de salsa de tomate\n2 dientes de ajo\nAceite de oliva\nSal y pimienta\nAlbahaca fresca",
                "1. Hervir agua con sal y cocinar la pasta al dente.\n2. Calentar aceite en una sartén y dorar el ajo picado.\n3. Agregar la salsa de tomate y cocinar 10 minutos a fuego medio.\n4. Mezclar la pasta con la salsa y servir con albahaca.",
            ),
            (
                "Ensalada César",
                "Ensalada fresca y cremosa, perfecta como entrada.",
                "1 lechuga romana\n100g de queso parmesano\nCrutones\n2 cucharadas de mayonesa\n1 limón\nSal y pimienta",
                "1. Lavar y trozar la lechuga.\n2. Preparar el aderezo mezclando mayonesa, jugo de limón, sal y pimienta.\n3. Mezclar la lechuga con el aderezo.\n4. Agregar crutones y parmesano rallado por encima.",
            ),
            (
                "Arroz con leche",
                "Postre tradicional reconfortante, cremoso y dulce.",
                "1 taza de arroz\n1 litro de leche\n3/4 taza de azúcar\n1 rama de canela\nCáscara de limón\nCanela en polvo",
                "1. Lavar el arroz y hervirlo 5 minutos en agua.\n2. Escurrir y agregar la leche, canela en rama y cáscara de limón.\n3. Cocinar a fuego bajo revolviendo frecuentemente por 30 minutos.\n4. Agregar el azúcar y cocinar 10 minutos más.\n5. Servir frío con canela en polvo.",
            ),
        ]
        cursor.executemany(
            "INSERT INTO recetas (nombre, descripcion, ingredientes, pasos) VALUES (?, ?, ?, ?)",
            recetas_ejemplo,
        )
        conn.commit()

    conn.close()