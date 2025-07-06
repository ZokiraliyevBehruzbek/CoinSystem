from flask import Blueprint, request, jsonify
from users.models import User


admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/add", methods=["POST"])
async def add_coin():
    data = request.form

    user_id = data.get("user_id")  # coin beriladigan foydalanuvchi ID
    superuser_id = data.get("is_superuser")  # coin berayotgan foydalanuvchi ID (adminmi yo'qmi)
    add_coins = data.get("coin")

    if not user_id or not add_coins or not superuser_id:
        return jsonify({"error": "Barcha maydonlar to'ldirilishi kerak"}), 400

    try:
        admin_user = await User.get(id=int(superuser_id))
    except:
        return jsonify({"error": "Admin foydalanuvchi topilmadi."}), 404

    if not admin_user.is_superuser:
        return jsonify({"error": "Sizda bu amalni bajarish huquqi yo'q!"}), 403

    try:
        target_user = await User.get(id=int(user_id))
    except:
        return jsonify({"error": "Target foydalanuvchi topilmadi."}), 404

    try:
        add_coins = int(add_coins)
    except:
        return jsonify({"error": "Coin raqam bo‘lishi kerak"}), 400

    # Coins ustunini yangilaymiz
    target_user.coins += add_coins
    await target_user.save()

    return jsonify({"message": f"{add_coins} coin muvaffaqiyatli qo‘shildi foydalanuvchi {target_user.username} ga."}), 200
