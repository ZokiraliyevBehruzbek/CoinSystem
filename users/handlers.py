from flask import Blueprint, request, jsonify
from users.models import User


user_bp = Blueprint("user", __name__)



@user_bp.route("/register", methods=["POST"])
async def register():
    data = request.form
    username = data.get("username")
    password = data.get("password")
    is_superuser = data.get("is_superuser")

    if is_superuser is None or is_superuser == "":
        is_superuser = False
    else:
        is_superuser = str(is_superuser).lower() == "true"


    if not username or not password:
        return jsonify({"error": "All fields are required"}), 400

    try:
        await User.create(username=username,password = password,is_superuser=is_superuser)
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@user_bp.route("/login", methods=["POST"])
async def login():
    data = request.form

    username = data.get("username")
    password = data.get("password")

    
    if not username or not password:
        return jsonify({"error": "Barcha maydonlar to'ldirilishi kerak"}), 400

    try:
        user = await User.get(username=username)
    except:
        return jsonify({"error": "Foydalanuvchi username topilmadi."}), 404

    if user.password != password:
        return jsonify({"error": "Parol noto‘g‘ri."}), 403
    
    coins = user.coins

    return jsonify({"message": f"Succesfully joined your avaible coins {coins}"})
