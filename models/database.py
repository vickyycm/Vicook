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

#crear tabla de categorías
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categorias (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre      TEXT    NOT NULL UNIQUE,
            descripcion TEXT
        )
    """)

#crear tabla de recetas con relación a categorías
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recetas (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre      TEXT    NOT NULL,
            descripcion TEXT    NOT NULL,
            ingredientes TEXT   NOT NULL,
            pasos       TEXT    NOT NULL,
            categoria_id INTEGER,
            FOREIGN KEY (categoria_id) REFERENCES categorias(id) ON DELETE SET NULL
        )
    """)
    conn.commit()

#solo insertar datos de ejemplo si las tablas están vacías
    if cursor.execute("SELECT COUNT(*) FROM categorias").fetchone()[0] == 0:
        categorias_ejemplo = [
            ("Desayuno", "Recetas para comenzar el día"),
            ("Almuerzo", "Platos principales para el almuerzo"),
            ("Cena", "Cenas ligeras o abundantes"),
            ("Postre", "Dulces y postres deliciosos"),
            ("Merienda", "Opciones para la merienda"),
        ]
        cursor.executemany(
            "INSERT INTO categorias (nombre, descripcion) VALUES (?, ?)",
            categorias_ejemplo,
        )
        conn.commit()

    if cursor.execute("SELECT COUNT(*) FROM recetas").fetchone()[0] == 0:
        cat_postre = cursor.execute("SELECT id FROM categorias WHERE nombre = 'Postre'").fetchone()[0]
        cat_almuerzo = cursor.execute("SELECT id FROM categorias WHERE nombre = 'Almuerzo'").fetchone()[0]
        cat_merienda = cursor.execute("SELECT id FROM categorias WHERE nombre = 'Merienda'").fetchone()[0]

        recetas_ejemplo = [
            (
                "Galletitas de café",
                "Galletitas crujientes con un toque de café, perfectas para acompañar tu bebida favorita.",
                "200g de manteca\n150g de azúcar\n1 huevo\n300g de harina\n2 cucharaditas de café instantáneo disuelto en 1 cucharada de agua caliente",
                "1. Batir la manteca y el azúcar hasta obtener una mezcla cremosa.\n2. Agregar el huevo y el café disuelto, mezclar bien.\n3. Incorporar la harina poco a poco hasta formar una masa homogénea.\n4. Formar bolitas con la masa, colocarlas en una bandeja para hornear y aplastarlas ligeramente.\n5. Hornear a 180°C por 12-15 minutos o hasta que estén doradas.",
                cat_merienda,
            ),
            (
                "Brownies",
                "Postre tradicional reconfortante, cremoso y dulce.",
                "200g de mantequilla\n150g de azúcar\n100g de chocolate\n2 huevos\n100g de harina\n1 cucharadita de polvo para hornear",
                "1. Derretir la mantequilla y el chocolate.\n2. Mezclar los ingredientes secos en un tazón.\n3. Batir los huevos y el azúcar hasta que estén espumosos.\n4. Incorporar la mezcla líquida a los ingredientes secos.\n5. Verter la mezcla en un molde y hornear a 180°C por 20-25 minutos.",
                cat_postre,
            ),
            (
                "Cookies",
                "Las cookies mas húmedas y al estilo nyc.",
                "200g de manteca\n150g de azucar mascabo\n80g de azucar\n400g de harina 0000\n2g de polvo para hornear\n150g de chocolate picado (aprox.)",
                "1. Mezclar la manteca y los azúcares hasta obtener una masa suave.\n2. Agregar los huevos y la vainilla.\n3. Incorporar la harina y el polvo para hornear.\n4. Agregar el chocolate picado.\n5. Formar cookies y hornear a 180°C por 10-12 minutos.",
                cat_postre,
            ),
            (
                "Noquis de calabaza",
                "Postre tradicional reconfortante, cremoso y dulce.",
                "200g de manteca\n150g de azúcar\n100g de calabaza cocida\n2 huevos\n100g de harina\n1 cucharadita de polvo para hornear",
                "1. Derretir la mantequilla y la calabaza cocida.\n2. Mezclar los ingredientes secos en un tazón.\n3. Batir los huevos y el azúcar hasta que estén espumosos.\n4. Incorporar la mezcla líquida a los ingredientes secos.\n5. Verter la mezcla en un molde y hornear a 180°C por 20-25 minutos.",
                cat_postre,
            ),
            (
                "Hambuguesas smash",
                "Hamburguesas al estilo neoyorquino, con una costra crujiente y un interior jugoso.",
                "500g de carne molida\nSal y pimienta al gusto\nPan de hamburguesa\nQueso cheddar\nLechuga, tomate, cebolla (opcional)",
                "1. Formar bolas con la carne molida y aplastarlas para formar hamburguesas delgadas.\n2. Cocinar en una sartén caliente hasta que estén doradas por ambos lados y el queso se derrita.\n3. Armar la hamburguesa con el pan, la carne, el queso y los vegetales al gusto.",
                cat_almuerzo,
            ),
        ]
        cursor.executemany(
            "INSERT INTO recetas (nombre, descripcion, ingredientes, pasos, categoria_id) VALUES (?, ?, ?, ?, ?)",
            recetas_ejemplo,
        )
        conn.commit()

    conn.close()