import requests
import uuid
import random
import time

BASE_URL = "http://127.0.0.1:8000"

def add_to_cart(user_id, product_id):
    cart_item_data = {"product_id": str(product_id), "quantity": random.randint(1, 5)}
    response = requests.post(f"{BASE_URL}/cart/{user_id}", json=cart_item_data)


def checkout(user_id):
    response = requests.post(f"{BASE_URL}/cart/{user_id}/checkout")


def main():
    user_id = uuid.uuid4()
    cart_products = []
    product_ids = [ product["id"] for product in requests.get(f"{BASE_URL}/products?limit=50").json()]
    
    print(f"Shopping started - User({user_id}) ")
    count = 0
    while True:
        random_id = product_ids[random.randint(0,49)]
        if random_id not in cart_products:
            add_to_cart(user_id, random_id)
            cart_products.append(random_id)
            count += 1
            print(f"({count}) Added to cart: {random_id} ")
            

        # Checkout randomly if there is 2-6 products in the cart
        if len(cart_products) >= random.randint(2, 6):
            checkout(user_id)
            cart_products = []
            print(f"Checkout completed ({count} items)! \n-----")
            count = 0

        time.sleep(1)


if __name__ == "__main__":
    main()
