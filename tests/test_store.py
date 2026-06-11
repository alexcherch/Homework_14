import pytest

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


def test_add_product(sample_category: Category) -> None:
    """Тест добавления продукта в категорию и обновление счетчиков."""
    new_product = Product("Xiaomi Redmi", "Бюджетный смартфон", 20000.0, 10)
    assert Category.product_count == 2
    sample_category.add_product(new_product)
    assert Category.product_count == 3


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


def test_category_products_getter(sample_category: Category) -> None:
    """Тест корректной работы геттера products."""
    expected_output = (
        "Samsung Galaxy, 50000.0 руб. Остаток: 5 шт.\n"
        "iPhone 15, 80000.0 руб. Остаток: 3 шт.\n"
    )
    assert sample_category.products == expected_output


def test_new_product_classmethod() -> None:
    """Тест создания объекта Product через класс-метод new_product."""
    product_dict = {"name": "Nokia 3310", "description": "Легендарный телефон", "price": 3000.0, "quantity": 100}

    product = Product.new_product(product_dict)

    assert product.name == "Nokia 3310"
    assert product.description == "Легендарный телефон"
    assert product.price == 3000.0
    assert product.quantity == 100


def test_new_product_merge_duplicates() -> None:
    """Тест слияния дубликатов товаров: сложение количества и выбор высшей цены."""
    existing_products = [Product("iPhone 15", "128GB", 80000.0, 5), Product("Samsung Galaxy", "256GB", 50000.0, 3)]

    duplicate_data = {"name": "iPhone 15", "description": "Новая партия", "price": 85000.0, "quantity": 3}

    result_product = Product.new_product(duplicate_data, existing_products)

    assert result_product.quantity == 8
    assert result_product.price == 85000.0


def test_new_product_no_duplicate_in_list() -> None:
    """Тест создания нового товара, если в списке его еще нет."""
    existing_products = [Product("iPhone 15", "128GB", 80000.0, 5)]

    new_data = {"name": "Xiaomi Redmi", "description": "Бюджетный", "price": 20000.0, "quantity": 10}

    result_product = Product.new_product(new_data, existing_products)

    assert result_product.name == "Xiaomi Redmi"
    assert result_product.quantity == 10
    assert result_product.price == 20000.0


def test_product_price_getter_and_setter() -> None:
    """Тест корректной работы геттера и установки валидной цены через сеттер."""
    product = Product("Телевизор", "4K", 50000.0, 2)

    assert product.price == 50000.0

    product.price = 55000.0
    assert product.price == 55000.0


def test_product_price_setter_invalid(capsys: pytest.CaptureFixture[str]) -> None:
    """Тест запрета установки нулевой или отрицательной цены."""
    product = Product("Телевизор", "4K", 50000.0, 2)

    product.price = -100.0

    assert product.price == 50000.0

    captured = capsys.readouterr()
    assert captured.out.strip() == "Цена не должна быть нулевая или отрицательная"


def test_product_price_setter_decrease_confirm(monkeypatch: pytest.MonkeyPatch) -> None:
    """Тест успешного снижения цены при согласии пользователя (ввод 'y')."""
    product = Product("Телевизор", "4K", 50000.0, 2)

    monkeypatch.setattr("builtins.input", lambda _: "y")

    product.price = 45000.0
    assert product.price == 45000.0


def test_product_price_setter_decrease_reject(monkeypatch: pytest.MonkeyPatch) -> None:
    """Тест отмены снижения цены при отказе пользователя (ввод 'n')."""
    product = Product("Телевизор", "4K", 50000.0, 2)

    monkeypatch.setattr("builtins.input", lambda _: "n")

    product.price = 45000.0
    assert product.price == 50000.0
