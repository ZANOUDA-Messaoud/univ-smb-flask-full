import json
import os
from flask import Flask, jsonify, request

app = Flask(__name__)

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

def get_db(filename):
    """Lit les données depuis un fichier JSON."""
    path = os.path.join(DATA_DIR, f"{filename}.json")
    if not os.path.exists(path):
        return []
    with open(path, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_db(filename, data):
    """Sauvegarde les données dans un fichier JSON."""
    path = os.path.join(DATA_DIR, f"{filename}.json")
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)


@app.route("/")
def index():
    """Route racine pour tester si l'API est en ligne."""
    return "L'API est en ligne ! Essayez d'acceder a /config/loadbalancer"

@app.route("/config/<type_cfg>", methods=['GET'])
def list_cfg(type_cfg):
    """Liste toutes les configurations d'un type donné."""
    # Note : type_cfg peut être 'webserver', 'reverseproxy' ou 'loadbalancer'
    return jsonify(get_db(type_cfg))

@app.route("/config/<type_cfg>/<int:id>", methods=['GET'])
def get_cfg(type_cfg, id):
    """Récupère un élément spécifique par son ID."""
    items = get_db(type_cfg)
    item = next((i for i in items if i['id'] == id), None)
    if item:
        return jsonify(item)
    return jsonify({"error": "Configuration non trouvée"}), 404

@app.route("/config/<type_cfg>", methods=['POST'])
def create_cfg(type_cfg):
    """Crée une nouvelle configuration."""
    items = get_db(type_cfg)
    new_item = request.json
    new_item['id'] = max([i['id'] for i in items], default=0) + 1
    items.append(new_item)
    save_db(type_cfg, items)
    return jsonify(new_item), 201

@app.route("/config/<type_cfg>/<int:id>", methods=['DELETE'])
def delete_cfg(type_cfg, id):
    """Supprime une configuration."""
    items = get_db(type_cfg)
    items = [i for i in items if i['id'] != id]
    save_db(type_cfg, items)
    return '', 204

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)