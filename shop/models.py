from tortoise import fields
from tortoise.models import Model


class Products(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50)
    description = fields.CharField(max_length=100)
    price = fields.FloatField(default = 0)


    def __str__(self):
        return self.name
