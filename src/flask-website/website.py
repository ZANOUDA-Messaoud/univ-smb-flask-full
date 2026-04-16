from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)

API_URL = "http://127.0.0.1:5001"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/servers")
def servers():
    res = requests.get(f"{API_URL}/servers")
    return render_template("servers.html", servers=res.json())


@app.route("/servers/<int:id>")
def server_detail(id):
    res = requests.get(f"{API_URL}/servers/{id}")
    server = res.json()

    config = f"""
server {{
    listen {server['port']};
    server_name {server['name']};

    location / {{
        proxy_pass http://localhost:{server['port']};
    }}
}}
"""
    return render_template("server_detail.html", config=config)


@app.route("/add_server", methods=["GET", "POST"])
def add_server():
    if request.method == "POST":
        data = {
            "name": request.form["name"],
            "port": int(request.form["port"])
        }
        requests.post(f"{API_URL}/servers", json=data)
        return redirect("/servers")

    return render_template("add_server.html")


@app.route("/delete_server/<int:id>")
def delete_server(id):
    requests.delete(f"{API_URL}/servers/{id}")
    return redirect("/servers")


if __name__ == "__main__":
    app.run(port=5000, debug=True)