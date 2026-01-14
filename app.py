from flask import Flask, render_template, request
import string
import secrets
import os   

app = Flask(__name__)


def generar_contrasena(longitud=12, usar_mayus=True, usar_minus=True, usar_numeros=True, usar_simbolos=True):


    "Genera un contraseña segura segun las opciones elegidas."
    caracteres = ""

    if usar_mayus:
        caracteres += string.ascii_uppercase

    if usar_minus:
        caracteres += string.ascii_lowercase

    if usar_numeros:
        caracteres += string.digits

    if usar_simbolos:
        caracteres += string.punctuation

    if not caracteres:
        raise ValueError("Debes seleccionar al menos un tipo de caracteres.")
    
    if longitud < 4:
        raise ValueError("la longitud minima recomendada es 4 caracteres.")
    
    # Generar la contraseña
    contrasena = ''.join(
        secrets.choice(caracteres)
        for _ in range(longitud)
    )
    return contrasena

@app.route("/", methods=["GET", "POST"])
def index():
    contrasena = None
    error = None

    if request.method == "POST":
        #Leer datos del formulario
        longitud_str = request.form.get("longitud", "12")

        try:
            longitud = int(longitud_str)
            if longitud <= 0:
                raise ValueError("la longitud debe ser mayor que 0.")
            
            usar_mayus = bool(request.form.get("usar_mayus"))
            usar_minus = bool(request.form.get("usar_minus"))
            usar_numeros = bool(request.form.get("usar_numeros"))
            usar_simbolos = bool(request.form.get("usar_simbolos"))

            contrasena = generar_contrasena(
                longitud=longitud,
                usar_mayus=usar_mayus,
                usar_minus=usar_minus,
                usar_numeros=usar_numeros,
                usar_simbolos=usar_simbolos,
            )
        except ValueError as e:
            error = str(e)
    
    return render_template("index.html", contrasena=contrasena, error=error)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)