from flask import Flask, render_template, request, jsonify
import os
import yaml
import joblib
import numpy as np
import json

params_path = "params.yaml"
webapp_root = "webapp"




class NumpyEncoder(json.JSONEncoder):
    """Special JSON encoder for numpyt type"""
    def default(self,obj):
        if isinstance(obj,np.integer):
            return int(obj)
        elif isinstance(obj,np.floating):
            return float(obj)
        elif isinstance(obj,np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self,obj)


def encode_to_json(data):
    encoded = json.dumps(data,cls=NumpyEncoder)
    # if as_py:
    #     return json.loads(encoded)
    return json.loads(encoded)


static_dir = os.path.join(webapp_root,'static')
template_dir = os.path.join(webapp_root,'templates')

app = Flask(__name__,static_folder=static_dir,template_folder=template_dir)

def read_params(config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
        return config

def predict(data):
    config = read_params(params_path)
    model_dir_path = config["webapp_model_dir"]
    model = joblib.load(model_dir_path)
    prediction = model.predict(data)
    print(prediction)
    return prediction


def api_response(request):
    try:
        data = np.array([list(request.json.values())])

        response = predict(data)
        response = encode_to_json(response)
        return response
    except Exception as e:
        print(e)
        error = {"Error":"Dont even try"}
        return error



@app.route("/",methods=['GET','POST'])
def index():
    if request.method == 'POST':
        try:
            if request.form:
                data = dict(request.form).values()
                data = [list(map(float,data))]
                response = predict(data)
                return render_template('index.html',response=response)
            elif request.json:
                response = api_response(request)
                return jsonify(response)

        except Exception as e:
            print(e)
            error = {"error":"Dont even try"}
            return render_template('404.html',error=error)
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)