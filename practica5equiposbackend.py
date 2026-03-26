from flask import Flask, jsonify, request

app = Flask("practica5equiposbackend")   

# --- MEMORIA (Fase 1) ---
inventario = [
    {"id": 1, "nombre": "Laptop", "precio": 800.0},
    {"id": 2, "nombre": "Mouse", "precio": 25.0}
]

# --- ENDPOINTS GET ---

@app.route('/equipo', methods=['GET'])
def function_equipo():
    return "Equipo Fabuloso de 2 personajes"

@app.route('/personajes', methods=['GET'])
def function_personajes():
    return "Personajes: 1. Fernando Loera, 2. Camilo Angulo"

@app.route('/productos', methods=['GET'])
def listar_productos():
    return jsonify(inventario), 200

# --- ENDPOINTS POST ---

@app.route('/productos', methods=['POST'])
def crear_producto():
    datos = request.get_json()
    
    nombre = datos.get('nombre')
    precio = datos.get('precio')

    # Validación (Requerimiento Fase 1)
    if precio <= 0:
        return jsonify({"error": "El precio debe ser mayor a 0"}), 400

    # Crear el nuevo producto con un ID único
    nuevo_id = len(inventario) + 1
    nuevo_item = {
        "id": nuevo_id,
        "nombre": nombre,
        "precio": precio
    }
    
    inventario.append(nuevo_item)
    return jsonify(nuevo_item), 201

@app.route('/post/user', methods=['POST'])
def function_user_post():
    req_json = request.get_json()
    username = req_json.get('username')
    password = req_json.get('password')
    print("Username: ", username)
    print("Password: ", password)
    print("-----------")
    return "POST REQUEST RECIBIDA", 200

    
app.run(port=3690)