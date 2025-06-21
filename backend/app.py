from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "✅ Chatbot médico premium corriendo correctamente"

@app.route("/webhook", methods=["POST"])
def whatsapp_reply():
    print("📩 Encabezados:")
    for k, v in request.headers.items():
        print(f"{k}: {v}")

    print("\n📩 Datos recibidos:")
    print(request.form)

    from_number = request.values.get('From', None)
    body = request.values.get('Body', '').strip()

    print("\n✅ Mensaje recibido:", body, "| De:", from_number)

    # Respuesta simple
    respuesta = "✅ ¡Hola! Soy tu asistente médico. ¿Qué síntomas tienes?"

    if "pecho" in body.lower():
        respuesta = "⚠️ Eso suena como una urgencia. Ve a urgencias 🏥"
    elif "cabeza" in body.lower():
        respuesta = "¿Desde cuándo te duele la cabeza? Podría ser migraña 🤕"
    elif "fiebre" in body.lower():
        respuesta = "¿Desde cuándo tienes fiebre? ¿Tienes tos o malestar? 🤒"

    # Generar respuesta Twilio
    resp = MessagingResponse()
    resp.message(respuesta)

    response_xml = str(resp)
    print("\n📤 XML enviado a Twilio:\n", response_xml)

    return Response(response_xml, mimetype="application/xml")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)

