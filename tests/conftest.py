import pytest
from src.store import Category, Product


@pytest.fixture(autouse=True)
def reset_category_counters():
    """Фикстура для сброса счетчиков класса перед каждым тестом."""
    Category.category_count = 0
    Category.product_count = 0


@pytest.fixture
def sample_products():
    """Фикстура для создания тестовых продуктов."""
    prod1 = Product("Samsung Galaxy", "Смартфон", 50000.0, 5)
    prod2 = Product("iPhone 15", "Смартфон", 80000.0, 3)
    return [prod1, prod2]


@pytest.fixture
def sample_category(sample_products):
    """Фикстура для создания тестовой категории."""
    return Category("Электроника", "Гаджеты", sample_products)
