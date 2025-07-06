from ariadne import MutationType
from fastapi import Request
from .models import product_collection
from .jwt_utils import verify_token

mutation = MutationType()

@mutation.field("createProduct")
def resolve_create_product(_, info, input):
    request: Request = info.context["request"]
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise Exception("Falta el token")

    token = auth_header.split(" ")[1]
    user = verify_token(token)

    product = {
        "name": input["name"],
        "description": input["description"],
        "price": input["price"],
        "brand": input["brand"],
        "created_by": user["email"]
    }

    product_collection.insert_one(product)
    return "Producto creado correctamente"
