from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/estado-estacionamiento', methods=['POST'])
def recibir_estado():
    datos = request.json
    print("\n" + "="*40)
    print("🚗 ¡DATOS DESDE WOKWI AL CONTENEDOR DOCKER! 🚗")
    print(f"Cajón 1: {'Ocupado' if datos.get('cajon1') == 1 else 'Libre'}")
    print(f"Cajón 2: {'Ocupado' if datos.get('cajon2') == 1 else 'Libre'}")
    print(f"Cajón 3: {'Ocupado' if datos.get('cajon3') == 1 else 'Libre'}")
    print("="*40 + "\n")
    return jsonify({"mensaje": "Datos recibidos en el contenedor al 100"}), 200

if __name__ == '__main__':
    # Usamos el puerto que la nube nos asigne, o el 5000 por defecto
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)