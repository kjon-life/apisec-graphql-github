from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
import strawberry
from .schema.types import Query

# Create Schema
schema = strawberry.Schema(query=Query)

# Create FastAPI app
app = FastAPI(title="SpaceX GraphQL Wrapper")

# Add GraphQL endpoint
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

@app.get("/")
async def root():
    return {"message": "SpaceX GraphQL API Wrapper", 
            "docs": "/graphql",
            "playground": "/graphql"} 