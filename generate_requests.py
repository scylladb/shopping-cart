import requests
import uuid
import random
import time

BASE_URL = "http://127.0.0.1:8000"


def upload_random_product():
    product_data = {
        "id": str(uuid.uuid4()),
        "name": f"Product {uuid.uuid4().hex[:8]}",
        "price": round(random.uniform(10.0, 100.0), 2),
        "img": "https://example.com/image.jpg",
    }
    response = requests.post(f"{BASE_URL}/products", json=product_data)
    print(f"New product: {product_data['name']}")
    return product_data["id"]


def add_to_cart(user_id, product_id):
    cart_item_data = {"product_id": str(product_id), "quantity": random.randint(1, 5)}
    response = requests.post(f"{BASE_URL}/cart/{user_id}", json=cart_item_data)
    print(f"Added to cart: {product_id} ")


def checkout(user_id):
    response = requests.post(f"{BASE_URL}/cart/{user_id}/checkout")
    print(f"User({user_id}) checkout completed! \n-----")


def main():
    user_id = uuid.uuid4()
    cart_products = []

    while True:
        product_id = upload_random_product()

        # Add 50% of the products to the cart
        if random.choice([True, False]):
            add_to_cart(user_id, product_id)
            cart_products.append(product_id)

        # Checkout randomly if there is 3-4 products in the cart
        if len(cart_products) >= random.randint(3, 5):
            checkout(user_id)
            cart_products = []

        time.sleep(1)


if __name__ == "__main__":
    main()
