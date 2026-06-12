import json
from pathlib import Path

from src.store import Category
from src.utils import load_data_from_json


def test_load_data_from_json(tmp_path: Path) -> None:
    """Тест корректности подгрузки данных из JSON-файла."""
    test_data = [
        {
            "name": "Смартфоны",
            "description": "Средство коммуникации",
            "products": [{"name": "Samsung Galaxy", "description": "256GB", "price": 180000.0, "quantity": 5}],
        }
    ]

    file_path = tmp_path / "products.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(test_data, f, ensure_ascii=False)

    categories = load_data_from_json(file_path)

    assert len(categories) == 1

    category = categories[0]
    assert isinstance(category, Category)
    assert category.name == "Смартфоны"
    assert category.description == "Средство коммуникации"

    expected_products_string = "Samsung Galaxy, 180000.0 руб. Остаток: 5 шт.\n"
    assert category.products == expected_products_string
