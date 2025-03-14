import json
import asyncio
from strawberry.printer import print_schema
from strawberry.schema.schema import Schema
from spacexdata.main import schema

async def generate_schema():
    # Get the schema as SDL (Schema Definition Language)
    schema_sdl = print_schema(schema)
    
    # Save the SDL schema
    with open('schema.graphql', 'w') as f:
        f.write(schema_sdl)
    print("SDL Schema has been generated as 'schema.graphql'")
    
    # Get the introspection schema
    introspection_query = """
    query IntrospectionQuery {
      __schema {
        queryType { name }
        mutationType { name }
        subscriptionType { name }
        types {
          ...FullType
        }
        directives {
          name
          description
          locations
          args {
            ...InputValue
          }
        }
      }
    }

    fragment FullType on __Type {
      kind
      name
      description
      fields(includeDeprecated: true) {
        name
        description
        args {
          ...InputValue
        }
        type {
          ...TypeRef
        }
        isDeprecated
        deprecationReason
      }
      inputFields {
        ...InputValue
      }
      interfaces {
        ...TypeRef
      }
      enumValues(includeDeprecated: true) {
        name
        description
        isDeprecated
        deprecationReason
      }
      possibleTypes {
        ...TypeRef
      }
    }

    fragment InputValue on __InputValue {
      name
      description
      type { ...TypeRef }
      defaultValue
    }

    fragment TypeRef on __Type {
      kind
      name
      ofType {
        kind
        name
        ofType {
          kind
          name
          ofType {
            kind
            name
            ofType {
              kind
              name
              ofType {
                kind
                name
                ofType {
                  kind
                  name
                }
              }
            }
          }
        }
      }
    }
    """
    
    # Execute introspection query
    result = await schema.execute(introspection_query)
    
    # Save the JSON introspection schema
    with open('schema.json', 'w') as f:
        json.dump(result.data, f, indent=2)
    print("JSON Introspection Schema has been generated as 'schema.json'")

if __name__ == "__main__":
    asyncio.run(generate_schema()) 