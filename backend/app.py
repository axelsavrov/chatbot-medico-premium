from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse
import pickle
import os

# Cargar modelo y vectorizador
with open("backend/vectorizador.pkl", "rb") as f:
    vectorizer = pickle.load(f)

with open("backend/modelo_sintomas.pkl", "rb") as f:
    modelo = pickle.load(f)

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "✅ Chatbot médico premium corriendo correctamente con IA"

@app.route("/webhook", methods=["POST"])
def whatsapp_reply():
    # Leer mensaje
    body = request.values.get('Body', '').strip()
    from_number = request.values.get('From', '')

    print(f"📥 Mensaje recibido: {body} | De: {from_number}")

    # Procesar con el modelo
    texto_vectorizado = vectorizer.transform([body])
    prediccion = modelo.predict(texto_vectorizado)[0]

    # Armar respuesta
    respuesta = f"🧠 Con base en lo que me dices, podrías requerir un especialista en: *{prediccion}*.\n¿Quieres que te asigne uno cercano?"

    # Enviar respuesta a WhatsApp
    resp = MessagingResponse()
    resp.message(respuesta)

    print("📤 Respuesta enviada:", respuesta)

    return Response(str(resp), mimetype="application/xml")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)


