from flask import Flask, render_template, request, redirect, session, send_file
import requests
import io

app = Flask(__name__)
app.secret_key = "secret"

API = "http://127.0.0.1:5001"


# -------- AUTH -------- #

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == "admin" and request.form["password"] == "admin":
            session["user"] = "admin"
            return redirect("/")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


def auth():
    return "user" in session


# -------- HOME -------- #

@app.route("/")
def index():
    if not auth():
        return redirect("/login")
    return render_template("index.html")


# -------- SERVERS -------- #

@app.route("/servers")
def servers():
    res = requests.get(f"{API}/servers")
    return render_template("servers.html", servers=res.json())


@app.route("/add_server", methods=["GET", "POST"])
def add_server():
    if request.method == "POST":
        name = request.form["name"]
        port = request.form["port"]

        if not name or not port:
            return "Erreur: champs obligatoires"

        requests.post(f"{API}/servers", json={
            "name": name,
            "port": int(port)
        })

        return redirect("/servers")

    return render_template("add_server.html")


# -------- PROXIES -------- #

@app.route("/proxies")
def proxies():
    res = requests.get(f"{API}/proxies")
    return render_template("proxies.html", proxies=res.json())


@app.route("/add_proxy", methods=["GET", "POST"])
def add_proxy():
    if request.method == "POST":
        requests.post(f"{API}/proxies", json={
            "name": request.form["name"],
            "target": request.form["target"]
        })
        return redirect("/proxies")

    return render_template("add_proxy.html")


# -------- LOAD BALANCER -------- #

@app.route("/loadbalancers")
def lbs():
    res = requests.get(f"{API}/loadbalancers")
    return render_template("lbs.html", lbs=res.json())


@app.route("/add_lb", methods=["GET", "POST"])
def add_lb():
    if request.method == "POST":
        servers = request.form["servers"].split(",")

        requests.post(f"{API}/loadbalancers", json={
            "name": request.form["name"],
            "servers": servers
        })

        return redirect("/loadbalancers")

    return render_template("add_lb.html")


# -------- DOWNLOAD CONFIG -------- #

@app.route("/download/server/<name>/<int:port>")
def download_config(name, port):
    config = f"""
server {{
    listen {port};
    server_name {name};

    location / {{
        proxy_pass http://localhost:{port};
    }}
}}
"""
    return send_file(
        io.BytesIO(config.encode()),
        download_name="nginx.conf",
        as_attachment=True
    )


if __name__ == "__main__":
    app.run(debug=True)