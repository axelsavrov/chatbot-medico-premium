from flask import Flask, jsonify
import json
import os

app = Flask(__name__)

# Función para cargar archivos JSON
def cargar_json(nombre_archivo):
    ruta = os.path.join(os.path.dirname(__file__), "../data", nombre_archivo)
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"error": f"{nombre_archivo} no encontrado"}
    except json.JSONDecodeError:
        return {"error": f"Error al leer {nombre_archivo}"}

# Endpoint: historial de pacientes
@app.route("/historial", methods=["GET"])
def obtener_historial():
    data = cargar_json("historial_pacientes.json")
    return jsonify(data)

# Endpoint: seguros registrados
@app.route("/seguros", methods=["GET"])
def obtener_seguros():
    data = cargar_json("seguros.json")
    return jsonify(data)

# Endpoint: hospitales disponibles
@app.route("/hospitales", methods=["GET"])
def obtener_hospitales():
    data = cargar_json("hospitales.json")
    return jsonify(data)

# Endpoint raíz para Render
@app.route("/", methods=["GET"])
def home():
    return "✅ Chatbot médico premium corriendo correctamente"

# Ejecución
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
