from flask import Flask, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "clave-local")


# =========================
# PRODUCTOS
# =========================

productos = [
    {
        "id": 1,
        "nombre": "Camiseta Premium",
        "categoria": "ropa",
        "descripcion": "Camiseta moderna y cómoda.",
        "precio": 59900,
        "icono": "👕"
    },
    {
        "id": 2,
        "nombre": "Camisa Casual",
        "categoria": "ropa",
        "descripcion": "Ideal para un estilo elegante.",
        "precio": 79900,
        "icono": "👔"
    },
    {
        "id": 3,
        "nombre": "Loción Premium",
        "categoria": "lociones",
        "descripcion": "Fragancia elegante y duradera.",
        "precio": 89900,
        "icono": "🧴"
    },
    {
        "id": 4,
        "nombre": "Loción Femenina",
        "categoria": "lociones",
        "descripcion": "Aroma fresco y sofisticado.",
        "precio": 99900,
        "icono": "🌸"
    },
    {
        "id": 5,
        "nombre": "Gorra Urbana",
        "categoria": "gorras",
        "descripcion": "Diseño moderno y versátil.",
        "precio": 39900,
        "icono": "🧢"
    },
    {
        "id": 6,
        "nombre": "Gorra Premium",
        "categoria": "gorras",
        "descripcion": "Diseño exclusivo para tu estilo.",
        "precio": 49900,
        "icono": "🧢"
    }
]


# =========================
# INICIO
# =========================

@app.route("/")
def inicio():
    return render_template("index.html")


# =========================
# CATEGORÍAS
# =========================

@app.route("/categoria/<categoria>")
def categoria(categoria):

    productos_categoria = [
        producto for producto in productos
        if producto["categoria"] == categoria
    ]

    nombres = {
        "ropa": "👕 Ropa",
        "lociones": "🧴 Lociones",
        "gorras": "🧢 Gorras"
    }

    nombre_categoria = nombres.get(categoria, "Productos")

    return render_template(
        "categoria.html",
        productos=productos_categoria,
        categoria=nombre_categoria
    )


# =========================
# AGREGAR AL CARRITO
# =========================

@app.route("/agregar/<int:producto_id>")
def agregar(producto_id):

    producto = next(
        (p for p in productos if p["id"] == producto_id),
        None
    )

    if producto:
        if "carrito" not in session:
            session["carrito"] = []

        carrito = session["carrito"]

        carrito.append(producto_id)

        session["carrito"] = carrito

    return redirect(url_for("carrito"))


# =========================
# CARRITO
# =========================

@app.route("/carrito")
def carrito():

    carrito_ids = session.get("carrito", [])

    productos_carrito = []

    for producto_id in carrito_ids:

        producto = next(
            (p for p in productos if p["id"] == producto_id),
            None
        )

        if producto:
            productos_carrito.append(producto)

    total = sum(
        producto["precio"]
        for producto in productos_carrito
    )

    return render_template(
        "carrito.html",
        productos=productos_carrito,
        total=total
    )


# =========================
# ELIMINAR DEL CARRITO
# =========================

@app.route("/eliminar/<int:producto_id>")
def eliminar(producto_id):

    carrito = session.get("carrito", [])

    if producto_id in carrito:
        carrito.remove(producto_id)

    session["carrito"] = carrito

    return redirect(url_for("carrito"))


# =========================
# FINALIZAR COMPRA
# =========================

@app.route("/checkout")
def checkout():

    carrito_ids = session.get("carrito", [])

    productos_carrito = []

    for producto_id in carrito_ids:

        producto = next(
            (p for p in productos if p["id"] == producto_id),
            None
        )

        if producto:
            productos_carrito.append(producto)

    total = sum(
        producto["precio"]
        for producto in productos_carrito
    )

    return render_template(
        "checkout.html",
        productos=productos_carrito,
        total=total
    )


# =========================
# EJECUTAR
# =========================
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)