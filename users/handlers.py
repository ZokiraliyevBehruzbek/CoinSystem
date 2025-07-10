from flask import Blueprint, request, jsonify
from users.models import User
from pydantic import ValidationError
from users.schemas import Register,Login

user_bp = Blueprint("user", __name__)



@user_bp.route("/register", methods=["POST"])
async def register():
    data = request.json
    try:
        users = Register(**data)
        try:
            await User.create(**users.model_dump())
            return jsonify({"message": "User registered successfully"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400  

@user_bp.route("/login", methods=["POST"])
async def login():
    data = request.json
    try:
        login_user = Login(**data)
        try:
            user = await User.get(username=login_user.username)
        except:
            return jsonify({"error": "Foydalanuvchi username topilmadi."}), 404

        if user.password != login_user.password:
            return jsonify({"error": "Parol noto‘g‘ri."}), 403
        
        coins = user.coins

        return jsonify({"message": f"Succesfully joined your avaible coins {coins}"})
    except ValidationError as e:
        return jsonify({"error": e.errors()})
    
