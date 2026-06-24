import json
from pathlib import Path
from typing import List,Dict

data_file = Path(__file__).parent.parent / "data" / "product.json"

def load_products() -> List[dict]:
    if not data_file.exists():
        return []
    with open(data_file,"r",encoding="utf-8") as file:
        return json.load(file)

def get_all_products() -> List[Dict]:
    return load_products()