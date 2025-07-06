from tortoise import fields
from tortoise.models import Model


class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True)
    password = fields.CharField(max_length=128)
    created_at = fields.DatetimeField(auto_now_add=True)
    is_superuser = fields.BooleanField(default=False)
    coins = fields.IntField(default = 0)

    def __str__(self):
        return self.username
