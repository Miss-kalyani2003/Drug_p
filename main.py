from flask import Flask,request,jsonify,render_template,send_from_directory
import config
import numpy as np
import os
import pymongo
import datetime
from flask_jwt_extended import jwt_required,create_access_token,JWTManager,get_jwt_identity
from src.util import Drug
from src.database import get_user_collection
Obj=Drug()

app=Flask(__name__)
user_collection=get_user_collection()

app.config["JWT_SECRET_KEY"]='secret-key'
jwt=JWTManager(app)

@app.route("/")
def Home():
    return render_template("login.html")

@app.route("/register_page")
def register_page():
    return render_template("register.html")

@app.route("/login_page")
def login_page():
    return render_template("login.html")

@app.route("/prediction_page")
def prediction_page():
    return render_template("prediction.html")

@app.route("/register",methods=['POST'])
def register():
    data=request.form
    user_name=data['user_name']
    password=data['password']
    email_id=data['email_id']
    contact_num=data['contact_num']

    response=user_collection.find_one({"email_id":email_id,"contact_num":contact_num})
    if not response:
        user_collection.insert_one({"user_name":user_name,"email_id":email_id,"contact_num":contact_num,"password":password,
                                    })
        return jsonify({"message":"user registed sucessfully"})
    else:
        print("user Already Exists")
        return jsonify({"message":"user Already Exists"})


@app.route("/login",methods=['POST'])
def login():
    data=request.form
    email_id=data['email_id']
    password=data['password']
    response=user_collection.find_one({"email_id":email_id,"password":password})
    if response:
        access_token=create_access_token(identity=email_id,expires_delta=datetime.timedelta(minutes=10))
        return jsonify({"status":"success","message":"Login sucessful","token":access_token})
    else:
        return jsonify({"status":"failure","message":"Invalid Credentials"})

@app.route("/prediction",methods=['POST'])
@jwt_required()
def prediction():
      data=request.form
      predicted_drug=Obj.predict_Drug(data)
      return {"predict Drug":f"{predicted_drug}"}


if __name__=="__main__":
    app.run(debug=True)


# from flask import Flask, request, jsonify
# import datetime
# from flask_jwt_extended import jwt_required, create_access_token, JWTManager
# from src.util import Drug
# from src.database import get_user_collection

# Obj = Drug()

# app = Flask(__name__)
# user_collection = get_user_collection()

# app.config["JWT_SECRET_KEY"] = "secret-key"
# jwt = JWTManager(app)


# @app.route("/")
# def Home():
#     return "Welcome to Drug API"


# @app.route("/register", methods=['POST'])
# def register():
#     # 👇 Use JSON instead of form (easier to debug)
#     data = request.get_json()
#     print("REGISTER DATA:", data)

#     user_name = data.get('user_name')
#     password = data.get('password')
#     email_id = data.get('email_id')
#     contact_num = data.get('contact_num')

#     if not all([user_name, password, email_id, contact_num]):
#         return jsonify({"message": "All fields are required"}), 400

#     # Check if user already exists (by email or contact)
#     response = user_collection.find_one({
#         "$or": [
#             {"email_id": email_id},
#             {"contact_num": contact_num}
#         ]
#     })
#     print("EXISTING USER:", response)

#     if not response:
#         user_collection.insert_one({
#             "user_name": user_name,
#             "email_id": email_id,
#             "contact_num": contact_num,
#             "password": password
#         })
#         return jsonify({"message": "user registered successfully"}), 201
#     else:
#         return jsonify({"message": "user already exists"}), 400


# @app.route("/login", methods=['POST'])
# def login():
#     data = request.get_json()
#     print("LOGIN DATA:", data)

#     user_name = data.get('user_name')
#     password = data.get('password')

#     if not all([user_name, password]):
#         return jsonify({"status": "failure", "message": "Username and password required"}), 400

#     # Find user by user_name + password
#     response = user_collection.find_one({
#         "user_name": user_name,
#         "password": password
#     })
#     print("USER FROM DB:", response)

#     if response:
#         access_token = create_access_token(
#             identity=user_name,
#             expires_delta=datetime.timedelta(minutes=10)
#         )
#         return jsonify({
#             "status": "success",
#             "message": "Login successful",
#             "token": access_token
#         }), 200
#     else:
#         return jsonify({"status": "failure", "message": "Invalid Credentials"}), 401


# @app.route("/prediction", methods=['POST'])
# @jwt_required()   # 👈 parentheses required
# def prediction():
#     data = request.get_json()
#     predicted_drug = Obj.predict_Drug(data)
#     return jsonify({"predict Drug": f"{predicted_drug}"})


# if __name__ == "__main__":
#     app.run(debug=True)
