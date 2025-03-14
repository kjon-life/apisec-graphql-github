from strawberry.printer import print_schema
from spacexdata.main import schema

def generate_sdl():
    # Get the schema as SDL (Schema Definition Language)
    schema_sdl = print_schema(schema)
    
    # Save the SDL schema
    with open('schema.graphql', 'w') as f:
        f.write(schema_sdl)
    print("SDL Schema has been generated as 'schema.graphql'")

if __name__ == "__main__":
    generate_sdl() 