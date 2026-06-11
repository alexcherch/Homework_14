from src.store import Category, Product


def test_product_init() -> None:
    """Тест корректности инициализации объекта класса Product."""
    product = Product("Samsung Galaxy", "Смартфон", 50000.0, 5)
    assert product.name == "Samsung Galaxy"
    assert product.description == "Смартфон"
    assert product.price == 50000.0
    assert product.quantity == 5


def test_category_init(sample_category: Category, sample_products: list[Product]) -> None:
    """Тест корректности инициализации объекта класса Category."""
    assert sample_category.name == "Электроника"
    assert sample_category.description == "Гаджеты"
    assert sample_category.products == sample_products


def test_category_and_product_count(sample_products: list[Product]) -> None:
    """Тест подсчета количества категорий и уникальных продуктов."""
    assert Category.category_count == 0
    assert Category.product_count == 0

    _ = Category("Электроника", "Гаджеты", sample_products)
    assert Category.category_count == 1
    assert Category.product_count == 2

    prod3 = Product("Преступление и наказание", "Книга", 500.0, 10)
    _ = Category("Книги", "Печатные издания", [prod3])

    assert Category.category_count == 2
    assert Category.product_count == 3
