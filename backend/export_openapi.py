import json
from app.main import app

def export_openapi():
    with open("openapi.json", "w") as f:
        json.dump(app.openapi(), f, indent=2)
    print("OpenAPI schema exported to openapi.json")

if __name__ == "__main__":
    export_openapi()
