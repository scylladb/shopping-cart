from scylladb import ScyllaClient
import config
from fastapi import FastAPI, Body, HTTPException
from pydantic import BaseModel
import uuid

app = FastAPI(
    title="ScyllaDB ecommerce sample application",
    contact={"url":"https://scylladb.com"}
)

client = ScyllaClient(config).get_session()

class Product(BaseModel):
    name: str
    price: float
    img: str
    

class CartItem(BaseModel):
    product_id: str
    

@app.get("/", tags=["home"])
def home():
    return {"Hello World!": "ScyllaDB Ecommerce sample application"}


@app.get("/products", tags=["products"])
def products(limit: int = 10):
    query = f"SELECT * FROM product LIMIT {limit};"
    return client.execute(query).all()


@app.get("/products/{product_id}", tags=["products"])
def product(product_id):
    query = "SELECT * FROM product WHERE id = %s;"
    return client.execute(query, [uuid.UUID(product_id), ]).one()


@app.get("/cart/{user_id}", tags=["cart"])
def cart(user_id):
    query = "SELECT * FROM active_cart WHERE user_id = %s;"
    return client.execute(query, [user_id]).all()


@app.post("/cart/{user_id}", tags=["cart"])
def add_to_cart(user_id, cart_item: CartItem):
    existing_cart = client.execute("SELECT * FROM active_cart WHERE user_id = %s", [user_id]).one()
    if existing_cart is None: # there's no cart created yet, create one
        query = "INSERT INTO active_cart (user_id, products) VALUES (%s, %s)"
        values = [user_id, set([uuid.UUID(cart_item.product_id)])]
        return client.execute(query, values)
    else: # there's already a cart, update it
        query = "UPDATE active_cart SET products= products + %s WHERE user_id = %s"
        values = [set([uuid.UUID(cart_item.product_id)]), user_id]
        return client.execute(query, values)


@app.delete("/cart/{user_id}", tags=["cart"])
def delete_from_cart(user_id, cart_item: CartItem):
    cart = client.execute("SELECT products FROM active_cart WHERE user_id = %s", [user_id]).one()
    if cart is None:
        raise HTTPException(status_code=404, detail="Item not found in cart")
    cart_items = cart["products"]
    product_id = uuid.UUID(cart_item.product_id)
    if product_id in cart_items:
        if len(cart_items) == 1:
            return client.execute("DELETE FROM active_cart WHERE user_id = %s", [user_id])
        else:
            cart_items.remove(product_id)
            return client.execute("UPDATE active_cart SET products=%s WHERE user_id = %s", [cart_items, user_id])
        


@app.post("/products", tags=["products"])
def upload_product(product: Product):
    query = "INSERT INTO product (id, name, price, img) VALUES (uuid(), %s, %s, %s)"
    values = list(product.model_dump().values())
    return client.execute(query, values)


@app.put("/products/{product_id}", tags=["products"])
def update_product(product: Product, product_id):
    body = product.model_dump()
    values = [body["name"], body["price"], body["img"], uuid.UUID(product_id)]
    query = "UPDATE product SET name=%s, price=%s, img=%s WHERE id = %s"
    return client.execute(query, values)


@app.delete("/products/{product_id}", tags=["products"])
def delete_product(product_id):
    query = "DELETE FROM product WHERE id = %s"
    return client.execute(query, [uuid.UUID(product_id)])


@app.post("/cart/{user_id}/checkout", tags=["cart"])
def checkout(user_id):
    # insert into orders table
    cart = client.execute("SELECT products FROM active_cart WHERE user_id = %s", [user_id]).one()
    if cart is None:
        raise HTTPException(status_code=404, detail="User's cart is empty")
    cart_items = cart["products"]
    query = "INSERT INTO orders (user_id, created_at, products) VALUES (%s, toTimestamp(now()), %s)"
    client.execute(query, [user_id, cart_items])
    
    # delete active cart
    client.execute("DELETE FROM active_cart WHERE user_id = %s", [user_id])



@app.get("/orders/{user_id}", tags=["orders"])
def orders(user_id):
    query = "SELECT * FROM orders WHERE user_id = %s;"
    return client.execute(query, [user_id]).all()
