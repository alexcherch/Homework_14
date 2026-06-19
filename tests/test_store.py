import pytest

from src.store import Category, Product, ProductIterator


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
    expected_output = "Samsung Galaxy, 50000.0 руб. Остаток: 5 шт.\n" "iPhone 15, 80000.0 руб. Остаток: 3 шт.\n"
    assert sample_category.products == expected_output


def test_new_product_classmethod() -> None:
    """Тест создания объекта Product через класс-метод new_product."""
    product_dict = {"name": "Nokia 3310", "description": "Легендарный телефон", "price": 3000.0, "quantity": 100}

    product = Product.new_product(product_dict)

    assert product.name == "Nokia 3310"
    assert product.description == "Легендарный телефон"
    assert product.price == 3000.0
    assert product.quantity == 100


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


def test_product_str() -> None:
    """Тест корректности строкового отображения объекта класса Product."""
    product = Product("Samsung Galaxy", "Смартфон", 50000.0, 5)
    assert str(product) == "Samsung Galaxy, 50000.0 руб. Остаток: 5 шт."


def test_category_str(sample_category: Category) -> None:
    """Тест корректности строкового отображения объекта класса Category."""
    assert str(sample_category) == "Электроника, количество продуктов: 8 шт."


def test_product_add(sample_products: list[Product]) -> None:
    """Тест сложения двух продуктов (подсчет суммарной стоимости запасов)."""
    # prod1: "Samsung Galaxy", цена 50000.0, количество 5 -> 250000.0
    # prod2: "iPhone 15", цена 80000.0, количество 3 -> 240000.0
    prod1, prod2 = sample_products

    assert prod1 + prod2 == 490000.0


def test_product_iterator(sample_category: Category) -> None:
    """Тест корректной работы вспомогательного класса ProductIterator."""
    iterator = ProductIterator(sample_category)

    products_from_iterator = []
    for product in iterator:
        products_from_iterator.append(product)

    assert len(products_from_iterator) == 2
    assert products_from_iterator[0].name == "Samsung Galaxy"
    assert products_from_iterator[1].name == "iPhone 15"
