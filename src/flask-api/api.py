from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)
DATA_PATH = "data"


def read_json(file):
    with open(os.path.join(DATA_PATH, file), "r") as f:
        return json.load(f)


def write_json(file, data):
    with open(os.path.join(DATA_PATH, file), "w") as f:
        json.dump(data, f, indent=4)


# -------- SERVERS -------- #

@app.route("/servers", methods=["GET"])
def get_servers():
    return jsonify(read_json("servers.json"))


@app.route("/servers", methods=["POST"])
def add_server():
    data = request.json
    servers = read_json("servers.json")

    new = {
        "id": len(servers) + 1,
        "name": data["name"],
        "port": data["port"]
    }

    servers.append(new)
    write_json("servers.json", servers)
    return jsonify(new)


@app.route("/servers/<int:id>", methods=["DELETE"])
def delete_server(id):
    servers = read_json("servers.json")
    servers = [s for s in servers if s["id"] != id]
    write_json("servers.json", servers)
    return jsonify({"message": "deleted"})


# -------- PROXIES -------- #

@app.route("/proxies", methods=["GET"])
def get_proxies():
    return jsonify(read_json("proxies.json"))


@app.route("/proxies", methods=["POST"])
def add_proxy():
    data = request.json
    proxies = read_json("proxies.json")

    new = {
        "id": len(proxies) + 1,
        "name": data["name"],
        "target": data["target"]
    }

    proxies.append(new)
    write_json("proxies.json", proxies)
    return jsonify(new)


@app.route("/proxies/<int:id>", methods=["DELETE"])
def delete_proxy(id):
    proxies = read_json("proxies.json")
    proxies = [p for p in proxies if p["id"] != id]
    write_json("proxies.json", proxies)
    return jsonify({"message": "deleted"})


# -------- LOAD BALANCERS -------- #

@app.route("/loadbalancers", methods=["GET"])
def get_lb():
    return jsonify(read_json("loadbalancers.json"))


@app.route("/loadbalancers", methods=["POST"])
def add_lb():
    data = request.json
    lbs = read_json("loadbalancers.json")

    new = {
        "id": len(lbs) + 1,
        "name": data["name"],
        "servers": data["servers"]
    }

    lbs.append(new)
    write_json("loadbalancers.json", lbs)
    return jsonify(new)


@app.route("/loadbalancers/<int:id>", methods=["DELETE"])
def delete_lb(id):
    lbs = read_json("loadbalancers.json")
    lbs = [l for l in lbs if l["id"] != id]
    write_json("loadbalancers.json", lbs)
    return jsonify({"message": "deleted"})


if __name__ == "__main__":
    app.run(port=5001, debug=True)