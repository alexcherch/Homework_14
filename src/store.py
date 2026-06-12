from __future__ import annotations


class Product:

    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

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
                user_choice = input(
                    f"Вы уверены, что хотите снизить цену с {self.__price} до {new_price}? (y/n): "
                )
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
            quantity=product_data["quantity"]
        )



class Category:
    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: list[Product]) -> None:
        self.name = name
        self.description = description
        self.__products = products

        Category.category_count += 1
        Category.product_count += len(products)

    def add_product(self, product: Product) -> None:
        """Специальный метод для добавления нового товара в приватный список."""
        self.__products.append(product)

        Category.product_count += 1

    @property
    def products(self) -> str:
        """Возвращает список товаров в виде отформатированных строк."""
        result_string = ""
        for product in self.__products:
            result_string += f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт.\n"
        return result_string
