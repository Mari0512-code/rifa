from flask import Flask, request, render_template
import barcode
from barcode.writer import ImageWriter
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        carnet = request.form.get("carnet")
        if not carnet:
            return "Error: Debe ingresar un número de carnet", 400

        # Generar código de barras
        code128 = barcode.get_barcode_class("code128")
        barcode_instance = code128(carnet, writer=ImageWriter())

        # Crear la ruta del archivo sin la extensión
        barcode_filename = f"{carnet}"
        barcode_path = os.path.join("static/barcodes", barcode_filename)

        # Asegurar que la carpeta exista
        os.makedirs("static/barcodes", exist_ok=True)

        # Depuración: Verificar que la ruta del archivo es correcta
        print(f"Guardando el código de barras en: {barcode_path}")

        # Guardar la imagen del código de barras
        barcode_instance.save(barcode_path)

        # Verificar que el archivo fue guardado
        if os.path.exists(barcode_path):
            print(f"Archivo guardado correctamente en: {barcode_path}")
        else:
            print("Error: El archivo no se guardó correctamente")

        return render_template("resultado.html", carnet=carnet, barcode_filename=barcode_filename)

    return render_template("index.html")

if __name__ == "__main__":
    # Asegurarse que la carpeta templates exista
    os.makedirs("templates", exist_ok=True)

    # Crear página de inicio (index.html)
    with open("templates/index.html", "w") as f:
        f.write("""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Página de Inicio</title>
</head>
<body>
    <h1>Bienvenido a la Generación de Códigos de Barras</h1>
    <form method="POST">
        <label for="carnet">Ingrese su carnet:</label>
        <input type="text" id="carnet" name="carnet" required>
        <button type="submit">Generar Código de Barras</button>
    </form>
</body>
</html>""")

    # Crear página de resultado (resultado.html)
    with open("templates/resultado.html", "w") as f:
        f.write("""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Resultado</title>
</head>
<body>
    <h1>Código de Barras Generado</h1>
    <p>Carnet: {{ carnet }}</p>
    <img src="/static/barcodes/{{ barcode_filename }}.png" alt="Código de Barras">
    <br>
    <a href="/">Generar otro código</a>
</body>
</html>""")

    app.run(debug=True)
