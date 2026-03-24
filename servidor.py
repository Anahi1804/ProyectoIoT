from flask import Flask, request, jsonify
from flask_cors import CORS  # <-- LÍNEA AGREGADA: Importamos los permisos
import Pyro5.api
import os

app = Flask(__name__)
CORS(app)  # <-- LÍNEA AGREGADA: Activamos los permisos para que la página web pueda entrar

# --- LUNA: PEGA AQUÍ EL DOMINIO .INTERNAL DE TU PYRO ---
# Ejemplo: "smart-parking-central.railway.internal"
HOST_INTERNO_PYRO = "proyectoiot-central.railway.internal"
PUERTO_PYRO = 9090 

@app.route('/estado-estacionamiento', methods=['POST'])
def recibir_estado():
    datos = request.json
    print("\n" + "="*40, flush=True)
    print("👩‍💼 Recepcionista (Flask): Recibí los datos del ESP32. Llamando al Gerente...", flush=True)
    
    # Extraemos los datos para mandarlos por teléfono
    c1 = datos.get('cajon1', 0)
    c2 = datos.get('cajon2', 0)
    c3 = datos.get('cajon3', 0)
    
    try:
        # Armamos el número de teléfono con la red privada
        uri = f"PYRO:estacionamiento.central@{HOST_INTERNO_PYRO}:{PUERTO_PYRO}"
        
        # Descolgamos el teléfono RMI
        servidor_central = Pyro5.api.Proxy(uri)
        
        # ¡LA MAGIA DISTRIBUIDA! Ejecutamos la función en el otro contenedor
        respuesta = servidor_central.actualizar_estado(c1, c2, c3)
        print(f"✅ El Gerente (Pyro) contestó: {respuesta}", flush=True)
        
    except Exception as e:
        print(f"❌ Error llamando al Gerente: {e}", flush=True)

    print("="*40 + "\n", flush=True)
    return jsonify({"mensaje": "Datos procesados por el sistema distribuido"}), 200

@app.route('/obtener-datos', methods=['GET'])
def obtener_datos():
    try:
        # Armamos el número del Gerente
        uri = f"PYRO:estacionamiento.central@{HOST_INTERNO_PYRO}:{PUERTO_PYRO}"
        servidor_central = Pyro5.api.Proxy(uri)
        
        # ¡Magia RMI! Le pedimos los datos directamente
        estado_actual = servidor_central.consultar_estado()
        
        # Se los mandamos a la página web
        return jsonify(estado_actual), 200
    except Exception as e:
        print(f"❌ Error consultando al Gerente: {e}", flush=True)
        return jsonify({"error": "No se pudo conectar con el cerebro"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
