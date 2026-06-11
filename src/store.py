from __future__ import annotations


class Product:

    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        self.name = name
        self.description = description
        self._price = price
        self.quantity = quantity

    @property
    def price(self) -> float:
        """Геттер для чтения цены товара."""
        return self._price

    @price.setter
    def price(self, new_price: float) -> None:
        """Сеттер для безопасной установки новой цены."""
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return

        if new_price >= self._price:
            self._price = new_price
            return

        user_choice = input(f"Вы уверены, что хотите снизить цену с {self._price} до {new_price}? (y/n): ")
        if user_choice.lower() == "y":
            self._price = new_price
            print("Цена успешно снижена.")
        else:
            print("Действие отменено. Цена осталась прежней.")

    @classmethod
    def new_product(cls, product_data: dict, all_products: list[Product] | None = None) -> Product:
        """
        Создает новый товар или обновляет существующий при совпадении имени.
        Складывает количество, выбирает наибольшую цену.
        """
        name = product_data["name"]
        description = product_data["description"]
        price = product_data["price"]
        quantity = product_data["quantity"]

        if all_products:
            for existing_product in all_products:
                if existing_product.name == name:
                    existing_product.quantity += quantity
                    if price > existing_product.price:
                        existing_product.price = price
                    return existing_product

        return cls(name, description, price, quantity)


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
