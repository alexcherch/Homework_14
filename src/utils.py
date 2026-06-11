import json
from pathlib import Path

from src.store import Category, Product


def load_data_from_json(file_path: str | Path) -> list[Category]:
    """Читает JSON-файл и возвращает список объектов класса Category."""
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    categories = []

    for category_data in data:
        products_list = []

        for product_data in category_data.get("products", []):
            product = Product(
                name=product_data["name"],
                description=product_data["description"],
                price=product_data["price"],
                quantity=product_data["quantity"],
            )
            products_list.append(product)

        category = Category(
            name=category_data["name"], description=category_data["description"], products=products_list
        )
        categories.append(category)

    return categories
