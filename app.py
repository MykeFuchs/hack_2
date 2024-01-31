from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from cerberus import Validator
import json


app = Flask(__name__)
CORS(app)
limiter = Limiter(get_remote_address)
limiter.init_app(app)


SCHEMA_CREATE_USER = {
    "email": {"type": "string", "required": True, "minlength": 3},
    "name": {"type": "string", "required": True, "minlength": 2},
    "age":{"type": "number", "required": True, "minlength": 1}
}
SCHEMA_GET_USER = {
    "email": {"type": "string", "required": True, "minlength": 3},
}

@app.before_request
def validate_customer():
    if request.path=="/user/create" and (request.method=="POST"):
        data = request.form.to_dict()
        profile = {
        "email":data["email"].strip(),
        "name":data["name"].strip(),
        "age": int(data["age"].strip())
    }

        checking= Validator(SCHEMA_CREATE_USER)
        if not checking.validate(profile):
            return {
                "payload": None,
                "error": checking.errors
            }   
        pass

    if request.path=="/v1/g/getuser" and request.method=="GET":
        email = {"email": request.args.get("email")}
        checking=Validator(SCHEMA_GET_USER)
        if not checking.validate(email):
            return {
                "payload": None,
                "error": checking.errors
            } 
            

@app.route("/user/create", methods=["POST"])
@limiter.limit("5/minute")
def fn_create_user():
    data=request.form.to_dict()
    json_path = "mock.json"

    profile = {
        "email":data["email"].strip(),
        "name":data["name"].strip(),
        "age": int(data["age"].strip()),
        "role": data["role"].strip()
    }

    with open(json_path,"r") as f:
        data_json = json.load(f)
    

    for user in data_json:
        if user["email"] == profile["email"]:
            return jsonify({
                "Payload": None,
                "error": "El usuario ya se encuentra registrado intente nuevamente." 
            })
        data_json.append(profile)

        with open(json_path,"w") as f:
            json.dump(data_json,f)
    
        return jsonify({
            "playload": profile,
            "error": None
        })


@app.route("/user/update", methods=["PUT"])
@limiter.limit("5/minutes")
def fn_update_user():
    data = request.form.to_dict()
    json_path = "mock.json"
    flag = 0

    profile = {
        "email":data["email"].strip(),
        "name":data["name"].strip(),
        "age": int(data["age"].strip()),
        "role": data["role"].strip()
    }

    with open(json_path, "r") as f:
        data_json = json.load(f)
    
    
    for i in range(len(data_json)):

        if data_json[i]["email"]==profile["email"]:
            data_json[i]=profile
            flag = 1

    if flag==0:
        return jsonify({
            "payload": None,
            "error": "No se pudo actualizar el usuario"
        })
    
    with open(json_path, "w") as f:
        json.dump(data_json,f)

        
    return jsonify({
            "playload": profile,
            "error": None
    })



@app.route("/v1/g/getuser", methods=["GET"])
@limiter.limit("5/minute")
def fn_get_user():
    json_path = "mock.json"
    email = request.args.get("email")
    obj_user={}


    with open(json_path,"r") as f:
        data_json = json.load(f)
    

    for user in data_json:
        if user["email"]== email: obj_user=user
    

    if obj_user=={}:
        return jsonify({
        "payload":None,
        "error": {
                "msg":"Usuario no existe"
                }
    })

    return jsonify({
        "payload":obj_user,
        "status": 200,
        "error": {
                "Active":None,
                "msg":None
                }
    })



@app.route("/v1/g/getuserall", methods=["GET"])
@limiter.limit("5/minute")
def fn_get_user_all():
    json_path = "mock.json"


    with open(json_path,"r") as f:
        data_json = json.load(f)
    


    if data_json==[]:
        return jsonify({
        "payload":None,
        "error": {
                "msg":"Tabla usuarios no existen"
                }
    })

    return jsonify({
        "payload":sorted(data_json,key= lambda data_json: int(data_json["age"])),
        "status": 200,
        "error": {
                "Active":None,
                "msg":None
                }
    })





if __name__ == '__main__':
    app.run(debug=True)

