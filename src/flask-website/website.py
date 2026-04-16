from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

API_URL = "http://localhost:5000/config"

@app.route("/")
def start(): 
    return render_template('start.html')

@app.route("/<type_cfg>/list")
def list_items(type_cfg):
    try:
        response = requests.get(f"{API_URL}/{type_cfg}")
        items = response.json()
    except Exception as e:
        print(f"Erreur de connexion à l'API : {e}")
        items = []
    return render_template('list.html', items=items, type_cfg=type_cfg)

@app.route("/<type_cfg>/view/<int:id>")
def view_config(type_cfg, id):
    try:
        item = requests.get(f"{API_URL}/{type_cfg}/{id}").json()
        
        sample_map = {
            "loadbalancer": "load-balancer",
            "reverseproxy": "reverse-proxy",
            "webserver": "webserver"
        }
        sample_file = sample_map.get(type_cfg, "webserver")
        
        # Lecture du template Nginx correspondant
        with open(f"nginx-templates/{sample_file}.sample", 'r') as f:
            content = f.read()
            

        config_generated = content.replace("example.com", item.get('name', 'serveur_inconnu'))
        
        return render_template('config_detail.html', config=config_generated, item=item, type_cfg=type_cfg)
    except Exception as e:
        return f"Erreur lors de la génération de la config : {e}", 500

@app.route("/<type_cfg>/create", methods=['GET', 'POST'])
def create_item(type_cfg):
    if request.method == 'POST':
        new_data = {
            "name": request.form.get('name'),
            "ip_bind": request.form.get('ip', '127.0.0.1')
        }
        requests.post(f"{API_URL}/{type_cfg}", json=new_data)
        return redirect(url_for('list_items', type_cfg=type_cfg))
    return render_template('add_form.html', type_cfg=type_cfg)

@app.route("/<type_cfg>/delete/<int:id>")
def delete_item(type_cfg, id):
    requests.delete(f"{API_URL}/{type_cfg}/{id}")
    return redirect(url_for('list_items', type_cfg=type_cfg))

if __name__ == "__main__":
    app.run(port=5001, debug=True)