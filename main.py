from flask import Flask
from users.handlers import user_bp
# from shop.handlers import shop_bp
from admin.handlers import admin_bp
from tortoise import Tortoise
from core.settings import TORTOISE_ORM
import asyncio



app = Flask(__name__)
app.register_blueprint(user_bp)
# app.register_blueprint(shop_bp)
app.register_blueprint(admin_bp)

# ORM-ni ishga tushurish
async def init_orm():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()

# ORM-ni yopish
async def close_orm():
    await Tortoise.close_connections()

if __name__ == "__main__":
    asyncio.run(init_orm())  # ORM ni boshlash
    try:
        app.run(debug=True)
    finally:
        asyncio.run(close_orm())
