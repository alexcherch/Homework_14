from __future__ import annotations

from abc import ABC, abstractmethod


class BaseProduct(ABC):
    """Абстрактный базовый класс для всех типов продуктов."""

    @abstractmethod
    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        """Абстрактный конструктор, задающий обязательные атрибуты продукта."""
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity
        super().__init__()

    @abstractmethod
    def __str__(self) -> str:
        """Абстрактный метод для строкового отображения продукта."""
        pass


class PrintMixin:
    """Класс-миксин для автоматического логирования создания объектов."""

    def __init__(self) -> None:
        """Конструктор миксина, который выводит лог и передает управление дальше."""
        print(repr(self))
        super().__init__()

    def __repr__(self) -> str:
        """Возвращает строковое представление объекта в виде ИмяКласса(атрибуты)."""
        price = getattr(self, f"_{self.__class__.__name__}__price", getattr(self, "_Product__price", 0))
        return f"{self.__class__.__name__}('{self.name}', '{self.description}', {price}, {self.quantity})"


class Product(BaseProduct, PrintMixin):
    """Класс, представляющий базовый продукт."""

    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        self.__price = price
        super().__init__(name=name, description=description, price=price, quantity=quantity)

    def __str__(self) -> str:
        """Строковое отображение продукта."""
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: Product) -> float:
        """Реализация сложения двух продуктов строго одного типа."""
        if type(self) is not type(other):
            raise TypeError("Нельзя складывать товары разных классов")

        return (self.price * self.quantity) + (other.price * other.quantity)

    @property
    def price(self) -> float:
        """Геттер для атрибута «цена» с использованием декоратора @property."""
        return self.__price

    @price.setter
    def price(self, new_price: float) -> None:
        """Для приватного атрибута «цена» реализован сеттер в классе Product
        с использованием декоратора @price.setter.
        """
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            if new_price >= self.__price:
                self.__price = new_price
            else:
                user_choice = input(f"Вы уверены, что хотите снизить цену с {self.__price} до {new_price}? (y/n): ")
                if user_choice.lower() == "y":
                    self.__price = new_price
                    print("Цена успешно снижена.")
                else:
                    print("Действие отменено. Цена осталась прежней.")

    @classmethod
    def new_product(cls, product_data: dict) -> Product:
        """Реализован класс-метод new_product() с помощью декоратора @classmethod."""
        return cls(
            name=product_data["name"],
            description=product_data["description"],
            price=product_data["price"],
            quantity=product_data["quantity"],
        )


class Smartphone(Product):
    """Класс-наследник класса Product для смартфонов."""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        efficiency: float,
        model: str,
        memory: int,
        color: str,
    ) -> None:
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    """Класс-наследник класса Product для газонной травы."""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: str,
        color: str,
    ) -> None:
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color


class Category:
    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: list[Product]) -> None:
        self._Category__products = None
        self.name = name
        self.description = description
        self.__products = products

        Category.category_count += 1
        Category.product_count += len(products)

    def __str__(self) -> str:
        """Строковое отображение категории со сквозным подсчетом всех единиц товаров."""
        total_quantity = 0
        for product in self.__products:
            total_quantity += product.quantity
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def add_product(self, product: Product) -> None:
        """Специальный метод для добавления нового товара в приватный список."""
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только продукты или их наследников")

        self.__products.append(product)
        Category.product_count += 1

    @property
    def products_list(self) -> list[Product]:
        """Геттер, который возвращает сам список объектов продуктов."""
        return self.__products

    @property
    def products(self) -> str:
        """Возвращает список товаров в виде отформатированных строк."""
        result_string = ""
        for product in self.__products:
            result_string += f"{product}\n"
        return result_string


class ProductIterator:

    def __init__(self, category: Category) -> None:
        """Конструктор принимает объект категории и инициализирует индекс."""
        self.products = category.products_list
        self.index = 0

    def __iter__(self) -> ProductIterator:
        """Метод __iter__ должен возвращать сам объект-итератор."""
        return self

    def __next__(self) -> Product:
        """Метод __next__ возвращает следующий товар или вызывает StopIteration."""
        if self.index < len(self.products):
            product = self.products[self.index]
            self.index += 1
            return product
        else:
            raise StopIteration
