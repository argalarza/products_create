from fastapi import FastAPI, Request
from ariadne import load_schema_from_path, make_executable_schema
from ariadne.asgi import GraphQL
from .resolvers import mutation

type_defs = load_schema_from_path("app/schema.graphql")
schema = make_executable_schema(type_defs, mutation)

app = FastAPI()
graphql_app = GraphQL(schema, context_value=lambda request: {"request": request})

app.mount("/", graphql_app)
