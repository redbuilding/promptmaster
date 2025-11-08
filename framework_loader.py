import json
import os

def load_frameworks(json_path="frameworks.json"):
    """Load framework definitions from JSON file."""
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Frameworks file not found: {json_path}")
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {fw["name"]: fw for fw in data["frameworks"]}