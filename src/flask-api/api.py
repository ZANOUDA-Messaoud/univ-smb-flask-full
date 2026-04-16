from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)

DATA_PATH = "data"


def read_json(filename):
    with open(os.path.join(DATA_PATH, filename), "r") as f:
        return json.load(f)


def write_json(filename, data):
    with open(os.path.join(DATA_PATH, filename), "w") as f:
        json.dump(data, f, indent=4)


# ---------------- SERVERS ---------------- #

@app.route("/servers", methods=["GET"])
def get_servers():
    return jsonify(read_json("servers.json"))


@app.route("/servers/<int:id>", methods=["GET"])
def get_server(id):
    servers = read_json("servers.json")
    for s in servers:
        if s["id"] == id:
            return jsonify(s)
    return jsonify({"error": "Not found"}), 404


@app.route("/servers", methods=["POST"])
def add_server():
    servers = read_json("servers.json")
    data = request.json

    new_server = {
        "id": len(servers) + 1,
        "name": data["name"],
        "port": data["port"]
    }

    servers.append(new_server)
    write_json("servers.json", servers)

    return jsonify(new_server), 201


@app.route("/servers/<int:id>", methods=["DELETE"])
def delete_server(id):
    servers = read_json("servers.json")
    servers = [s for s in servers if s["id"] != id]
    write_json("servers.json", servers)

    return jsonify({"message": "Deleted"})
    

if __name__ == "__main__":
    app.run(port=5001, debug=True)