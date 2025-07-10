from flask import Blueprint, request, jsonify
from shop.models import Products
from shop.schemas import CreateSchema,PaginationSchema,RemoveSchemas
from pydantic import ValidationError
from users.models import User

shop_bp = Blueprint("products", __name__)



@shop_bp.route("/create", methods=["POST"])
async def create():
    data = request.json
    try:
        product_create = CreateSchema(**data)
        try:
            await Products.create(**product_create.model_dump())
            return jsonify({"message": "Product successfully created"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

@shop_bp.route("/remove", methods=["POST"])
async def remove():
    data = request.json
    try:
        remove_product = RemoveSchemas(**data)
        # Adminni tekshiramiz
        try:
            admin_user = await User.get(id=int(remove_product.is_superuser))
        except:
            return jsonify({"error": "Bunday foydalanuvchi mavjud emas!"}), 404

        if not admin_user.is_superuser:
            return jsonify({"error": "Siz admin emassiz!"}), 403

        # Mahsulotni topamiz
        try:
            product = await Products.get(name=str(remove_product.name))
        except:
            return jsonify({"error": "Bunday mahsulot topilmadi!"}), 404

        # Mahsulotni o‘chiramiz
        await product.delete()
        return jsonify({"message": "Mahsulot o‘chirildi!"}), 200

    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400



@shop_bp.route("/all", methods=["POST"])
async def get_products_paginated():
    data = request.get_json()

    try:
        pagination = PaginationSchema(**data)  
        offset = (pagination.page - 1) * pagination.per_page

        total = await Products.all().count()
        products = await Products.all().offset(offset).limit(pagination.per_page)

        results = []
        for product in products:
            results.append({
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": product.price
            })

        return jsonify({
            "total": total,
            "page": pagination.page,
            "per_page": pagination.per_page,
            "products": results
        })
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
